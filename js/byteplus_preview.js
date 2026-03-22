// import { app } from "../../scripts/app.js";

// app.registerExtension({
//     name: "BytePlus.VideoPreview",
//     async beforeRegisterNodeDef(nodeType, nodeData, app) {
//         // Убеждаемся, что добавляем плеер только в нашу кастомную ноду
//         if (nodeData.name === "BytePlusVideoGenNode") {
//             const onExecuted = nodeType.prototype.onExecuted;
            
//             nodeType.prototype.onExecuted = function (message) {
//                 if (onExecuted) {
//                     onExecuted.apply(this, arguments);
//                 }

//                 // Наш Python-код отправляет message.videos
//                 if (message?.videos) {
//                     const video = message.videos[0];
//                     // Формируем внутреннюю ссылку ComfyUI на сохраненный файл
//                     const videoUrl = `/view?filename=${encodeURIComponent(video.filename)}&type=${video.type}`;

//                     // Ищем виджет плеера, если его еще нет — создаем 🏗️
//                     let videoWidget = this.widgets?.find(w => w.name === "video_player");
                    
//                     if (!videoWidget) {
//                         const videoEl = document.createElement("video");
//                         videoEl.controls = true; // Показываем кнопки play/pause
//                         videoEl.loop = true;     // Зацикливаем
//                         videoEl.autoplay = true; // Автостарт
//                         videoEl.muted = true;    // Без звука для стабильного автоплея в браузере
//                         videoEl.style.width = "100%";
//                         videoEl.style.marginTop = "10px";
//                         videoEl.style.borderRadius = "8px"; // Немного красоты 🎨
                        
//                         videoWidget = this.addDOMWidget("video_player", "video", videoEl);
//                     }
                    
//                     // Обновляем ссылку на новое видео
//                     videoWidget.element.src = videoUrl;
//                 }
//             };
//         }
//     }
// });