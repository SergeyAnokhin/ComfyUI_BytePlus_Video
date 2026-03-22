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
                    "seedance-1-0-lite-i2v-250428", # Самая дешевая для тестов 📉
                    "seedance-1-5-pro-251215", 
                    "seedance-1-0-pro-fast-251015"
                ], {"default": "seedance-1-0-lite-i2v-250428"}),
                "resolution": (["480p", "720p", "1080p"], {"default": "720p"}),
                "ratio": (["adaptive", "16:9", "4:3", "1:1", "3:4", "9:16", "21:9"], {"default": "adaptive"}),
                "duration": ([5, 10, 12], {"default": 5}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff}), # -1 для рандома 🎲
                "camera_fixed": ("BOOLEAN", {"default": False}),
                "generate_audio": ("BOOLEAN", {"default": False}),
                "watermark": ("BOOLEAN", {"default": False}),
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

    def generate_and_download(self, image, prompt, api_key, model_id, resolution, ratio, duration, seed, camera_fixed, generate_audio, watermark):
        client = Ark(base_url="https://ark.ap-southeast.bytepluses.com/api/v3", api_key=api_key)
        base64_img = self.tensor_to_base64(image)

        # Обработка сида
        actual_seed = int(time.time()) if seed == -1 else seed

        print(f"🎬 [BytePlus] Запуск {model_id} (Seed: {actual_seed})...")
        
        # Сбор параметров для запроса
        payload = {
            "model": model_id,
            "resolution": resolution,
            "ratio": ratio,
            "duration": duration,
            "seed": actual_seed,
            "camera_fixed": camera_fixed,
            "generate_audio": generate_audio,
            "watermark": watermark,
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": base64_img}}
            ]
        }

        create_result = client.content_generation.tasks.create(**payload)
        task_id = create_result.id
        start_time = time.time()

        while True:
            res = client.content_generation.tasks.get(task_id=task_id)
            elapsed = int(time.time() - start_time)
            
            if res.status == "succeeded":
                print(f"✅ Готово за {elapsed}с")
                # Используем путь, который мы нашли через дебаг 🔍
                video_url = res.content.video_url
                break
            elif res.status == "failed":
                raise Exception(f"❌ Ошибка API: {res.error}")
            
            print(f"⏳ Генерируем ({model_id})... {elapsed}с")
            time.sleep(5)

        # Скачивание файла 📥
        file_name = f"BytePlus_{int(time.time())}.mp4"
        full_path = os.path.join(self.output_dir, file_name)
        
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(full_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return {"ui": {"videos": [{"filename": file_name, "type": "output"}]}, "result": (file_name,)}