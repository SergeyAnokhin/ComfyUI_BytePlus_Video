import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "BytePlus.URLVideoPlayer",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "URLVideoPlayerNode") {
            const onExecuted = nodeType.prototype.onExecuted;
            
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                
                if (message?.b_video_urls) {
                    let url = message.b_video_urls[0];
                    
                    // 🪄 МАГИЯ ЗДЕСЬ: Проверяем, это веб-ссылка или локальный файл
                    if (!url.startsWith("http")) {
                        // На всякий случай отрезаем "C:\...", если вдруг пришел полный путь
                        const cleanFilename = url.split('\\').pop().split('/').pop();
                        // Формируем правильную внутреннюю ссылку ComfyUI
                        url = `/view?filename=${encodeURIComponent(cleanFilename)}&type=output`;
                    }
                    
                    let vidWidget = this.widgets?.find(w => w.name === "html_player");
                    
                    if (!vidWidget) {
                        const vidEl = document.createElement("video");
                        vidEl.controls = true;
                        vidEl.autoplay = true;
                        vidEl.muted = true;
                        vidEl.loop = true;
                        vidEl.style.width = "100%";
                        vidEl.style.borderRadius = "8px";
                        vidEl.style.marginTop = "10px";
                        
                        vidWidget = this.addDOMWidget("html_player", "video", vidEl);
                    }
                    
                    // Загружаем видео (локально или из сети)
                    vidWidget.element.src = url;
                    this.onResize?.(this.size);
                }
            };
        }
    }
});