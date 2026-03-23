import base64
import copy
import json
import os
import time
from io import BytesIO

import comfy.utils
import folder_paths
import numpy as np
import requests
from byteplussdkarkruntime import Ark
from PIL import Image


class BytePlusVideoGen:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "A cinematic video..."}),
                "api_key": ("STRING", {"default": "YOUR_API_KEY_HERE"}),
                "model_id": (
                    [
                        "seedance-1-0-lite-i2v-250428",
                        "seedance-1-5-pro-251215",
                        "seedance-1-0-pro-fast-251015",
                    ],
                    {"default": "seedance-1-0-lite-i2v-250428"},
                ),
                "resolution": (["480p", "720p", "1080p"], {"default": "720p"}),
                "ratio": (
                    ["none", "adaptive", "16:9", "4:3", "1:1", "3:4", "9:16", "21:9"],
                    {"default": "none"},
                ),
                "duration": ("INT", {"default": 5, "min": 2, "max": 12, "step": 1}),
                "camera_fixed": ("BOOLEAN", {"default": False}),
                "generate_audio": ("BOOLEAN", {"default": False}),
                "watermark": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "first_image": ("IMAGE",),
                "last_image": ("IMAGE",),
                "ref_image_1": ("IMAGE",),
                "ref_image_2": ("IMAGE",),
                "ref_image_3": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("filename", "full_filepath", "video_url")
    OUTPUT_NODE = True
    FUNCTION = "generate_and_download"
    CATEGORY = "BytePlus/Video"

    def tensor_to_base64(self, single_image_tensor):
        i = 255.0 * single_image_tensor.cpu().numpy()
        img = Image.fromarray(np.uint8(i))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    def generate_and_download(
        self,
        prompt,
        api_key,
        model_id,
        resolution,
        ratio,
        duration,
        camera_fixed,
        generate_audio,
        watermark,
        first_image=None,
        last_image=None,
        ref_image_1=None,
        ref_image_2=None,
        ref_image_3=None,
    ):
        client = Ark(base_url="https://ark.ap-southeast.bytepluses.com/api/v3", api_key=api_key)

        content_items = [{"type": "text", "text": prompt}]

        if first_image is not None:
            print("[BytePlus] Added first frame.")
            first_frame_data = {"type": "image_url", "image_url": {"url": self.tensor_to_base64(first_image[0])}}

            if last_image is not None:
                print("[BytePlus] Added last frame.")
                first_frame_data["role"] = "first_frame"
                content_items.append(first_frame_data)
                content_items.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": self.tensor_to_base64(last_image[0])},
                        "role": "last_frame",
                    }
                )
            else:
                content_items.append(first_frame_data)
        elif last_image is not None:
            print("[BytePlus] last_image ignored because first_image is missing.")

        ref_list = [img for img in [ref_image_1, ref_image_2, ref_image_3] if img is not None]
        if ref_list:
            print("[BytePlus] Processing reference images...")
            for ref_batch in ref_list:
                for i in range(ref_batch.shape[0]):
                    content_items.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": self.tensor_to_base64(ref_batch[i])},
                            "role": "reference_image",
                        }
                    )

        payload = {
            "model": model_id,
            "resolution": resolution,
            "duration": duration,
            "camera_fixed": camera_fixed,
            "generate_audio": generate_audio,
            "watermark": watermark,
            "content": content_items,
        }

        if ratio != "none":
            payload["ratio"] = ratio

        debug_payload = copy.deepcopy(payload)
        for item in debug_payload.get("content", []):
            if item.get("type") == "image_url":
                item["image_url"]["url"] = "<base64_data_truncated_for_logs>"

        print("\n[BytePlus] Request payload:")
        print(json.dumps(debug_payload, indent=2, ensure_ascii=False))
        print("-" * 40 + "\n")

        print(f"[BytePlus] Starting task ({model_id})...")
        create_result = client.content_generation.tasks.create(**payload)
        task_id = create_result.id
        start_time = time.time()

        pbar = comfy.utils.ProgressBar(100)
        current_progress = 0

        while True:
            res = client.content_generation.tasks.get(task_id=task_id)
            elapsed = int(time.time() - start_time)

            if res.status == "succeeded":
                pbar.update_absolute(100, 100)
                print(f"[BytePlus] Generation completed in {elapsed}s")
                video_url = res.content.video_url
                print(f"[BytePlus] Video URL: {video_url}")

                print("\n[BytePlus] Full model response:")
                try:
                    if hasattr(res, "model_dump"):
                        print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
                    elif hasattr(res, "dict"):
                        print(json.dumps(res.dict(), indent=2, ensure_ascii=False))
                    else:
                        print(str(res))
                except Exception:
                    print(str(res))
                print("-" * 40 + "\n")
                break

            if res.status == "failed":
                raise Exception(f"BytePlus API error: {res.error}")

            if current_progress < 95:
                current_progress += 5
            pbar.update_absolute(current_progress, 100)

            print(f"[BytePlus] Waiting ({model_id})... {elapsed}s | status: {res.status}")
            time.sleep(5)

        file_name = f"BytePlus_{int(time.time())}.mp4"
        full_path = os.path.join(self.output_dir, file_name)

        print(f"[BytePlus] Saving video to: {full_path}")
        with requests.get(video_url, stream=True) as response:
            response.raise_for_status()
            with open(full_path, "wb") as file_obj:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    file_obj.write(chunk)

        print(f"[BytePlus] File saved: {full_path}")
        return {"ui": {"videos": [{"filename": file_name, "type": "output"}]}, "result": (file_name, full_path, video_url)}
