import os
import time
import base64
import torch
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from byteplussdkarkruntime import Ark
import folder_paths 

class BytePlusVideoGen:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",), 
                "prompt": ("STRING", {"multiline": True, "default": "A cinematic video..."}),
                "api_key": ("STRING", {"default": "YOUR_API_KEY_HERE"}),
                "model_id": (["seedance-1-5-pro-251215", "seedance-1-0-pro-fast-251015"],),
                "resolution": (["720p", "1080p"], {"default": "720p"}),
                "duration": ([5, 10], {"default": 5}),
                "filename_prefix": ("STRING", {"default": "BytePlus_Video"}),
            },
        }

    RETURN_TYPES = ("STRING",) 
    RETURN_NAMES = ("filename",)
    OUTPUT_NODE = True 
    FUNCTION = "generate_and_download"
    CATEGORY = "BytePlus/Video"

    def tensor_to_base64(self, image_tensor):
        i = 255. * image_tensor[0].cpu().numpy()
        img = Image.fromarray(np.uint8(i))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"

    def generate_and_download(self, image, prompt, api_key, model_id, resolution, duration, filename_prefix):
        client = Ark(base_url="https://ark.ap-southeast.bytepluses.com/api/v3", api_key=api_key)
        base64_img = self.tensor_to_base64(image)

        print(f"🎬 [BytePlus] Отправка запроса на генерацию...")
        create_result = client.content_generation.tasks.create(
            model=model_id,
            resolution=resolution,
            duration=duration,
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": base64_img}}
            ]
        )

        task_id = create_result.id
        video_url = None
        start_time = time.time() # Фиксируем время старта для таймера ⏱️

        # 🔄 Цикл ожидания с улучшенным логированием
        while True:
            res = client.content_generation.tasks.get(task_id=task_id)
            elapsed = int(time.time() - start_time) # Считаем секунды
            
            if res.status == "succeeded":
                print(f"✅ [BytePlus] Готово! Время выполнения: {elapsed}с")
                
                # Достаем ссылку из правильного места, которое мы нашли в дебаге
                try:
                    if hasattr(res, 'content') and res.content:
                        video_url = res.content.video_url
                        print(f"🔗 Ссылка найдена: {video_url[:50]}...")
                    else:
                        print(f"❌ Поле 'content' отсутствует. Доступные поля: {list(res.__dict__.keys())}")
                        raise AttributeError("URL видео не найден в объекте content")
                except Exception as e:
                    print(f"⚠️ Ошибка при извлечении URL: {e}")
                    raise e
                break
                
            elif res.status == "failed":
                raise Exception(f"❌ Ошибка BytePlus: {res.error}")
            
            # Меняющееся сообщение с таймером ⏳
            print(f"⏳ Генерируем... {elapsed}с | Статус: {res.status}")
            time.sleep(4)

        # 📥 Скачивание
        print(f"📥 [BytePlus] Загрузка файла...")
        file_name = f"{filename_prefix}_{int(time.time())}.mp4"
        full_path = os.path.join(self.output_dir, file_name)

        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*1024): # Чанки по 1МБ
                    f.write(chunk)
            print(f"🚀 Видео успешно сохранено в: {full_path}")
        else:
            raise Exception(f"Ошибка скачивания: статус {response.status_code}")

        return {"ui": {"videos": [{"filename": file_name, "type": "output"}]}, "result": (file_name,)}