from .byteplus_video_gen_node import BytePlusVideoGen
from .byteplus_url_player_node import URLVideoPlayer
from .byteplus_llm_node import BytePlusLLMChat

NODE_CLASS_MAPPINGS = {
    "BytePlusVideoGenNode": BytePlusVideoGen,
    "URLVideoPlayerNode": URLVideoPlayer,
    "BytePlusLLMChatNode": BytePlusLLMChat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BytePlusVideoGenNode": "📹 BytePlus Video Generator (Ark)",
    "URLVideoPlayerNode": "📺 BytePlus Video Player",
    "BytePlusLLMChatNode": "🧠 BytePlus LLM Chat (Ark)",
}

# ⚠️ САМОЕ ВАЖНОЕ ДЛЯ JAVASCRIPT:
WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]