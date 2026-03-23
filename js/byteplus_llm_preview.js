import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "BytePlus.LLMPreview",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "BytePlusLLMChatNode") {
            const onExecuted = nodeType.prototype.onExecuted;

            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                const llmText =
                    (Array.isArray(message?.llm_text) ? message.llm_text[0] : message?.llm_text) ??
                    (Array.isArray(message?.ui?.llm_text) ? message.ui.llm_text[0] : message?.ui?.llm_text);

                if (!llmText) {
                    return;
                }

                let widget = this.widgets?.find((w) => w.name === "llm_result_preview");
                if (!widget) {
                    widget = this.addWidget("text", "llm_result_preview", "", () => {}, {
                        multiline: true,
                    });
                    if (widget?.inputEl) {
                        widget.inputEl.readOnly = true;
                        widget.inputEl.style.minHeight = "160px";
                    }
                }

                widget.value = llmText;
                this.onResize?.(this.size);
            };
        }
    },
});
