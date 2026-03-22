from .byteplus_video_node import BytePlusVideoGen, URLVideoPlayer

NODE_CLASS_MAPPINGS = {
    "BytePlusVideoGenNode": BytePlusVideoGen,
    "URLVideoPlayerNode": URLVideoPlayer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BytePlusVideoGenNode": "📹 BytePlus Video Generator (Ark)",
    "URLVideoPlayerNode": "📺 BytePlus Video Player"
}

# ⚠️ САМОЕ ВАЖНОЕ ДЛЯ JAVASCRIPT:
WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']