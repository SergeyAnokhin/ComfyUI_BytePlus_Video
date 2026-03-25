import json
import time

import comfy.utils
from byteplussdkarkruntime import Ark


TEXT_GENERATION_MODELS = [
    "seed-2-0-lite-260228",
    "seed-2-0-mini-260215",
    "seed-1-8-251228",
    "glm-4-7-251222",
    "deepseek-v3-2-251201",
    "deepseek-v3-1-250821",
    "seed-1-6-250915",
    "seed-1-6-250615",
    "seed-1-6-flash-250715",
    "seed-1-6-flash-250615",
    "kimi-k2-thinking-251104",
    "kimi-k2-250905",
    "kimi-k2-250711",
    "deepseek-v3-250324",
    "skylark-pro-250415",
]

PRICING_TABLE = {
    "seed-2-0-lite": [
        {"max_k": 128, "input": 0.25, "output": 2.00},
        {"max_k": 256, "input": 0.50, "output": 4.00},
    ],
    "seed-2-0-mini": [
        {"max_k": 128, "input": 0.10, "output": 0.40},
        {"max_k": 256, "input": 0.20, "output": 0.80},
    ],
    "seed-1-8": [
        {"max_k": 128, "input": 0.25, "output": 2.00},
        {"max_k": 256, "input": 0.50, "output": 4.00},
    ],
    "glm-4-7": [{"max_k": None, "input": 0.60, "output": 2.20}],
    "deepseek-v3-2": [
        {"max_k": 32, "input": 0.28, "output": 0.42},
        {"max_k": 128, "input": 0.56, "output": 0.84},
    ],
    "deepseek-v3-1": [{"max_k": None, "input": 0.56, "output": 1.68}],
    "seed-1-6": [
        {"max_k": 128, "input": 0.25, "output": 2.00},
        {"max_k": 256, "input": 0.50, "output": 4.00},
    ],
    "seed-1-6-flash": [
        {"max_k": 128, "input": 0.075, "output": 0.30},
        {"max_k": 256, "input": 0.10, "output": 0.80},
    ],
    "skylark-pro": [{"max_k": None, "input": 0.40, "output": 1.60}],
    "kimi-k2": [{"max_k": None, "input": 0.60, "output": 2.50}],
    "deepseek-v3": [{"max_k": None, "input": 1.14, "output": 4.56}],
}


def _extract_usage_tokens(usage_obj):
    if usage_obj is None:
        return 0, 0, 0

    if hasattr(usage_obj, "model_dump"):
        usage = usage_obj.model_dump()
    elif hasattr(usage_obj, "dict"):
        usage = usage_obj.dict()
    elif isinstance(usage_obj, dict):
        usage = usage_obj
    else:
        usage = {}

    input_tokens = int(usage.get("prompt_tokens", usage.get("input_tokens", 0)) or 0)
    output_tokens = int(usage.get("completion_tokens", usage.get("output_tokens", 0)) or 0)
    total_tokens = int(usage.get("total_tokens", input_tokens + output_tokens) or (input_tokens + output_tokens))
    return input_tokens, output_tokens, total_tokens


def _normalize_model_for_pricing(model_id):
    if model_id.startswith("seed-2-0-lite"):
        return "seed-2-0-lite"
    if model_id.startswith("seed-2-0-mini"):
        return "seed-2-0-mini"
    if model_id.startswith("seed-1-8"):
        return "seed-1-8"
    if model_id.startswith("glm-4-7"):
        return "glm-4-7"
    if model_id.startswith("deepseek-v3-2"):
        return "deepseek-v3-2"
    if model_id.startswith("deepseek-v3-1"):
        return "deepseek-v3-1"
    if model_id.startswith("seed-1-6-flash"):
        return "seed-1-6-flash"
    if model_id.startswith("seed-1-6"):
        return "seed-1-6"
    if model_id.startswith("kimi-k2"):
        return "kimi-k2"
    if model_id.startswith("skylark-pro"):
        return "skylark-pro"
    if model_id.startswith("deepseek-v3"):
        return "deepseek-v3"
    return None


def _estimate_cost_usd(model_id, input_tokens, output_tokens):
    pricing_key = _normalize_model_for_pricing(model_id)
    if pricing_key not in PRICING_TABLE:
        return 0.0

    tiers = PRICING_TABLE[pricing_key]
    input_k_tokens = input_tokens / 1000.0
    selected_tier = tiers[-1]
    for tier in tiers:
        max_k = tier.get("max_k")
        if max_k is None or input_k_tokens <= max_k:
            selected_tier = tier
            break

    input_cost = (input_tokens / 1_000_000.0) * selected_tier["input"]
    output_cost = (output_tokens / 1_000_000.0) * selected_tier["output"]
    return input_cost + output_cost


def _content_to_text(content):
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                text_value = item.get("text")
                if text_value:
                    text_parts.append(str(text_value))
        return "\n".join(text_parts)
    return str(content)


class BytePlusLLMChat:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompt": ("STRING", {"multiline": True, "default": "Summarize this text in bullet points."}),
                "api_key": ("STRING", {"default": "YOUR_API_KEY_HERE"}),
                "model_id": (TEXT_GENERATION_MODELS, {"default": "seed-1-6-flash-250715"}),
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
                "structured_output_mode": (["none", "json_object", "json_schema"], {"default": "none"}),
                "json_schema_name": ("STRING", {"default": "structured_response", "advanced": True, "tooltip": "Name for the structured output (used if structured_output_mode is 'json_schema')"}),
                "json_schema_strict": ("BOOLEAN", {"default": True, "advanced": True, "tooltip": "Strict schema adherence"}),
                "json_schema": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": '{\n  "type": "object",\n  "properties": {\n    "summary": {"type": "string"},\n    "items": {\n      "type": "array",\n      "items": {"type": "string"}\n    }\n  },\n  "required": ["summary", "items"],\n  "additionalProperties": false\n}',
                        "advanced": True,
                        "tooltip": "JSON Schema for structured response (used if structured_output_mode is 'json_schema')",
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT", "INT", "INT", "FLOAT")
    RETURN_NAMES = (
        "response_text",
        "reasoning_text",
        "raw_response_json",
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "estimated_cost_usd",
    )
    OUTPUT_NODE = True
    FUNCTION = "run_llm"
    CATEGORY = "BytePlusVideo/Text"

    def run_llm(
        self,
        user_prompt,
        api_key,
        model_id,
        system_prompt,
        disable_thinking,
        temperature,
        max_tokens,
        structured_output_mode,
        json_schema_name,
        json_schema_strict,
        json_schema,
    ):
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

        if structured_output_mode == "json_object":
            payload["response_format"] = {"type": "json_object"}
        elif structured_output_mode == "json_schema":
            try:
                schema_obj = json.loads(json_schema)
            except Exception as exc:
                raise Exception(f"json_schema is not valid JSON: {exc}")
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": (json_schema_name or "structured_response").strip() or "structured_response",
                    "schema": schema_obj,
                    "strict": bool(json_schema_strict),
                },
            }

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
            response_text = _content_to_text(message.content).strip() if hasattr(message, "content") else ""
            reasoning_text = (message.reasoning_content or "").strip() if hasattr(message, "reasoning_content") else ""

        input_tokens, output_tokens, total_tokens = _extract_usage_tokens(getattr(completion, "usage", None))
        estimated_cost_usd = _estimate_cost_usd(model_id, input_tokens, output_tokens)

        raw_json = ""
        if hasattr(completion, "model_dump"):
            raw_json = json.dumps(completion.model_dump(), indent=2, ensure_ascii=False)
        elif hasattr(completion, "dict"):
            raw_json = json.dumps(completion.dict(), indent=2, ensure_ascii=False)
        else:
            raw_json = str(completion)

        preview_lines = [
            f"Model: {model_id}",
            f"Latency: {elapsed}s",
            f"Structured output: {structured_output_mode}",
            f"Tokens (in/out/total): {input_tokens}/{output_tokens}/{total_tokens}",
            f"Estimated cost (USD): {estimated_cost_usd:.8f}",
            "",
            response_text or "<empty response>",
        ]
        preview_text = "\n".join(preview_lines)

        pbar.update_absolute(100, 100)
        print(f"[BytePlus LLM] Completed in {elapsed}s")

        return {
            "ui": {"llm_text": [preview_text]},
            "result": (
                response_text,
                reasoning_text,
                raw_json,
                input_tokens,
                output_tokens,
                total_tokens,
                float(estimated_cost_usd),
            ),
        }
