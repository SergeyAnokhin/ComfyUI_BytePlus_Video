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
                "model_id": ([
                    "seedance-1-0-lite-i2v-250428", 
                    "seedance-1-5-pro-251215", 
                    "seedance-1-0-pro-fast-251015"
                ], {"default": "seedance-1-0-lite-i2v-250428"}),
                "resolution": (["480p", "720p", "1080p"], {"default": "720p"}),
                "ratio": (["adaptive", "16:9", "4:3", "1:1", "3:4", "9:16", "21:9"], {"default": "adaptive"}),
                "duration": ("INT", {"default": 5, "min": 2, "max": 12, "step": 1}),
                "camera_fixed": ("BOOLEAN", {"default": False}),
                "generate_audio": ("BOOLEAN", {"default": False}),
                "watermark": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "reference_images": ("IMAGE",), 
            }
        }

    RETURN_TYPES = ("STRING",) 
    RETURN_NAMES = ("filename",)
    OUTPUT_NODE = True 
    FUNCTION = "generate_and_download"
    CATEGORY = "BytePlus/Video"

    def tensor_to_base64(self, single_image_tensor):
        i = 255. * single_image_tensor.cpu().numpy()
        img = Image.fromarray(np.uint8(i))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"

    def generate_and_download(self, image, prompt, api_key, model_id, resolution, ratio, duration, camera_fixed, generate_audio, watermark, reference_images=None):
        client = Ark(base_url="https://ark.ap-southeast.bytepluses.com/api/v3", api_key=api_key)
        
        # 1. Основное изображение
        content_items = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": self.tensor_to_base64(image[0])}} 
        ]

        # 2. Добавление референсов (только для Lite модели)
        if reference_images is not None and "lite-i2v" in model_id:
            num_refs = reference_images.shape[0]
            print(f"🎬 [BytePlus] Добавляем {num_refs} референсов...")
            for i in range(num_refs):
                content_items.append({"type": "image_url", "image_url": {"url": self.tensor_to_base64(reference_images[i])}})

        # 3. Payload без параметра seed
        payload = {
            "model": model_id,
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "camera_fixed": camera_fixed,
            "generate_audio": generate_audio,
            "watermark": watermark,
            "content": content_items
        }

        print(f"🎬 [BytePlus] Запуск {model_id} (Длительность: {duration}с)...")
        create_result = client.content_generation.tasks.create(**payload)
        task_id = create_result.id
        start_time = time.time()

        while True:
            res = client.content_generation.tasks.get(task_id=task_id)
            elapsed = int(time.time() - start_time)
            
            if res.status == "succeeded":
                print(f"✅ Готово за {elapsed}с")
                video_url = res.content.video_url
                break
            elif res.status == "failed":
                raise Exception(f"❌ Ошибка API: {res.error}")
            
            print(f"⏳ Генерируем ({model_id})... {elapsed}с | Статус: {res.status}")
            time.sleep(5)

        # 4. Сохранение файла
        file_name = f"BytePlus_{int(time.time())}.mp4"
        full_path = os.path.join(self.output_dir, file_name)
        
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(full_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return {"ui": {"videos": [{"filename": file_name, "type": "output"}]}, "result": (file_name,)}