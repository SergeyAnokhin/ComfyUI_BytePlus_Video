import os
import time
import base64
import copy
import torch
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from byteplussdkarkruntime import Ark
import folder_paths 
import comfy.utils

class BytePlusVideoGen:
    def __init__(self):
        # Получаем путь к папке output ComfyUI
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "A cinematic video..."}),
                "api_key": ("STRING", {"default": "YOUR_API_KEY_HERE"}),
                "model_id": ([
                    "seedance-1-0-lite-i2v-250428", 
                    "seedance-1-5-pro-251215", 
                    "seedance-1-0-pro-fast-251015"
                ], {"default": "seedance-1-0-lite-i2v-250428"}),
                "resolution": (["480p", "720p", "1080p"], {"default": "720p"}),
                "ratio": (["none", "adaptive", "16:9", "4:3", "1:1", "3:4", "9:16", "21:9"], {"default": "none"}),
                "duration": ("INT", {"default": 5, "min": 2, "max": 12, "step": 1}),
                "camera_fixed": ("BOOLEAN", {"default": False}),
                "generate_audio": ("BOOLEAN", {"default": False}),
                "watermark": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "first_image": ("IMAGE",),      # Начальный кадр (опционально)
                "last_image": ("IMAGE",),       # Конечный кадр (опционально)
                "ref_image_1": ("IMAGE",),      # Референс 1 (опционально)
                "ref_image_2": ("IMAGE",),      # Референс 2 (опционально)
                "ref_image_3": ("IMAGE",),      # Референс 3 (опционально)
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING") 
    RETURN_NAMES = ("filename", "full_filepath", "video_url")
    OUTPUT_NODE = True 
    FUNCTION = "generate_and_download"
    CATEGORY = "BytePlus/Video"

    def tensor_to_base64(self, single_image_tensor):
        """Конвертация тензора изображения в Base64 для API"""
        i = 255. * single_image_tensor.cpu().numpy()
        img = Image.fromarray(np.uint8(i))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"

    def generate_and_download(self, prompt, api_key, model_id, resolution, ratio, duration, 
                              camera_fixed, generate_audio, watermark, 
                              first_image=None, last_image=None, 
                              ref_image_1=None, ref_image_2=None, ref_image_3=None):
        
        client = Ark(base_url="https://ark.ap-southeast.bytepluses.com/api/v3", api_key=api_key)
        
        # 1. Формируем список контента, начиная с текста
        content_items = [{"type": "text", "text": prompt}]

        # 2. Логика первого и последнего кадра
        if first_image is not None:
            print("📸 [BytePlus] Добавлен первый кадр.")
            first_frame_data = {"type": "image_url", "image_url": {"url": self.tensor_to_base64(first_image[0])}}
            
            # Добавляем последний кадр ТОЛЬКО если есть первый
            if last_image is not None:
                print("📸 [BytePlus] Добавлен последний кадр.")
                first_frame_data["role"] = "first_frame"
                content_items.append(first_frame_data)
                content_items.append({"type": "image_url", "image_url": {"url": self.tensor_to_base64(last_image[0])}, "role": "last_frame"})
            else:
                # Если только первая картинка, роль не указываем (по документации API)
                content_items.append(first_frame_data)
        elif last_image is not None:
            # Условие: Игнорируем last_image, если нет first_image
            print("⚠️ [BytePlus] Внимание: last_image проигнорирован, так как не указан first_image!")

        # 3. Добавляем референсы (поддержка до 3 слотов + батчи внутри каждого)
        ref_list = [img for img in [ref_image_1, ref_image_2, ref_image_3] if img is not None]
        if ref_list:
            print(f"🎨 [BytePlus] Обработка референсных изображений...")
            for ref_batch in ref_list:
                for i in range(ref_batch.shape[0]):
                    content_items.append({"type": "image_url", "image_url": {"url": self.tensor_to_base64(ref_batch[i])}, "role": "reference_image"})

        # 4. Сборка параметров запроса
        payload = {
            "model": model_id,
            "resolution": resolution,
            "duration": duration,
            "camera_fixed": camera_fixed,
            "generate_audio": generate_audio,
            "watermark": watermark,
            "content": content_items
        }

        # Добавляем ratio только если оно не "none"
        if ratio != "none":
            payload["ratio"] = ratio

        # --- ЛОГИРОВАНИЕ ПАРАМЕТРОВ ЗАПРОСА (ОБРЕЗКА BASE64) ---
        debug_payload = copy.deepcopy(payload)
        for item in debug_payload.get("content", []):
            if item.get("type") == "image_url":
                item["image_url"]["url"] = "<base64_data_truncated_for_logs>"
        
        print(f"\n📋 [BytePlus] ОТПРАВЛЯЕМЫЕ ПАРАМЕТРЫ:")
        import json
        print(json.dumps(debug_payload, indent=2, ensure_ascii=False))
        print("-" * 40 + "\n")
        # --------------------------------------------------------

        print(f"🚀 [BytePlus] Запуск задачи ({model_id})...")
        create_result = client.content_generation.tasks.create(**payload)
        task_id = create_result.id
        start_time = time.time()

        pbar = comfy.utils.ProgressBar(100)
        current_progress = 0

        # 5. Ожидание результата
        while True:
            res = client.content_generation.tasks.get(task_id=task_id)
            elapsed = int(time.time() - start_time)
            
            if res.status == "succeeded":
                pbar.update_absolute(100, 100)                
                print(f"✅ [BytePlus] Генерация завершена за {elapsed}с")
                video_url = res.content.video_url
                print(f"🔗 Ссылка на видео (URL): {video_url}")
                
                # --- ЛОГИРОВАНИЕ ПОЛНОГО ОТВЕТА МОДЕЛИ ---
                print(f"\n📊 [BytePlus] ПОЛНЫЙ ОТВЕТ МОДЕЛИ:")
                try:
                    import json
                    # Пытаемся вывести в красивом JSON формате
                    if hasattr(res, 'model_dump'):
                        print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
                    elif hasattr(res, 'dict'):
                        print(json.dumps(res.dict(), indent=2, ensure_ascii=False))
                    else:
                        print(str(res))
                except Exception:
                    print(str(res))
                print("-" * 40 + "\n")
                # ----------------------------------------
                
                break
            elif res.status == "failed":
                raise Exception(f"❌ Ошибка BytePlus API: {res.error}")
            
            if current_progress < 95:
                current_progress += 5
            pbar.update_absolute(current_progress, 100)

            print(f"⏳ Ожидание ({model_id})... {elapsed}с | Статус: {res.status}")
            time.sleep(5)

        # 6. Сохранение файла на диск 📥
        file_name = f"BytePlus_{int(time.time())}.mp4"
        full_path = os.path.join(self.output_dir, file_name)
        
        print(f"📂 Видео будет сохранено в: {full_path}")
        
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(full_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    f.write(chunk)

        print(f"💾 Файл успешно записан на диск: {full_path}")

        # Возвращаем 1: Полный путь к файлу, 2: URL
        # СЕКРЕТНЫЙ ТРЮК: Меняем "videos" на "gifs", чтобы ComfyUI автоматически 
        # включил встроенный плеер прямо внутри нашей ноды! 🍿
        return {"ui": {"videos": [{"filename": file_name, "type": "output"}]}, "result": (file_name, full_path, video_url)}
    

class URLVideoPlayer:
    """
    Простая нода, которая берет STRING (URL или путь) 
    и передает его в интерфейс для воспроизведения.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_url": ("STRING", {"forceInput": True}), # Принудительно ждем провод STRING
            }
        }

    RETURN_TYPES = () # Ничего не выводим дальше
    OUTPUT_NODE = True # Сообщаем ComfyUI, что это финальная нода (чтобы запускался процесс)
    FUNCTION = "play_video"
    CATEGORY = "BytePlus/Video"

    def play_video(self, video_url):
        print(f"📺 [Player] Получена ссылка для плеера: {video_url}")
        # Отправляем ссылку нашему JavaScript файлу
        return {"ui": {"b_video_urls": [video_url]}}    