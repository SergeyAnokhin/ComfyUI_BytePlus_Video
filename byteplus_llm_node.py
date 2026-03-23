import json
import time

import comfy.utils
from byteplussdkarkruntime import Ark


class BytePlusLLMChat:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompt": ("STRING", {"multiline": True, "default": "Summarize this text in bullet points."}),
                "api_key": ("STRING", {"default": "YOUR_API_KEY_HERE"}),
                "model_id": ("STRING", {"default": "seed-1-6-flash-250715"}),
                "system_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "You are a helpful assistant.",
                    },
                ),
                "disable_thinking": ("BOOLEAN", {"default": True}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 1024, "min": 1, "max": 32768, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("response_text", "reasoning_text", "raw_response_json")
    OUTPUT_NODE = True
    FUNCTION = "run_llm"
    CATEGORY = "BytePlus/Text"

    def run_llm(self, user_prompt, api_key, model_id, system_prompt, disable_thinking, temperature, max_tokens):
        pbar = comfy.utils.ProgressBar(100)
        pbar.update_absolute(5, 100)

        client = Ark(base_url="https://ark.ap-southeast.bytepluses.com/api/v3", api_key=api_key)
        pbar.update_absolute(15, 100)

        messages = []
        if system_prompt and system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt.strip()})
        messages.append({"role": "user", "content": user_prompt})

        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if disable_thinking:
            payload["thinking"] = {"type": "disabled"}

        debug_payload = dict(payload)
        print("\n[BytePlus LLM] Request payload:")
        print(json.dumps(debug_payload, indent=2, ensure_ascii=False))
        print("-" * 40 + "\n")

        pbar.update_absolute(30, 100)
        start = time.time()
        completion = client.chat.completions.create(**payload)
        elapsed = int(time.time() - start)

        pbar.update_absolute(85, 100)

        message = completion.choices[0].message if completion.choices else None
        response_text = ""
        reasoning_text = ""
        if message is not None:
            response_text = (message.content or "").strip() if hasattr(message, "content") else ""
            reasoning_text = (message.reasoning_content or "").strip() if hasattr(message, "reasoning_content") else ""

        raw_json = ""
        if hasattr(completion, "model_dump"):
            raw_json = json.dumps(completion.model_dump(), indent=2, ensure_ascii=False)
        elif hasattr(completion, "dict"):
            raw_json = json.dumps(completion.dict(), indent=2, ensure_ascii=False)
        else:
            raw_json = str(completion)

        preview_lines = [f"Model: {model_id}", f"Latency: {elapsed}s", "", response_text or "<empty response>"]
        preview_text = "\n".join(preview_lines)

        pbar.update_absolute(100, 100)
        print(f"[BytePlus LLM] Completed in {elapsed}s")

        return {
            "ui": {"llm_text": [preview_text]},
            "result": (response_text, reasoning_text, raw_json),
        }
