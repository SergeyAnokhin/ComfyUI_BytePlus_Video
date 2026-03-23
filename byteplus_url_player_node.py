class URLVideoPlayer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "play_video"
    CATEGORY = "BytePlus/Tools"

    def play_video(self, video_url):
        print(f"[Player] Received URL for player: {video_url}")
        return {"ui": {"b_video_urls": [video_url]}}
