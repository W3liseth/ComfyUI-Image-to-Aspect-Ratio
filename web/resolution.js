import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "AspectRatioLatent.Resolution",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "AspectRatioEmptyLatent") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            onNodeCreated?.apply(this, arguments);
            this.resolutionPreview = this.addWidget(
                "button", "Resolution after execution", null, () => {}, { serialize: false }
            );
        };

        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
            onExecuted?.apply(this, arguments);
            if (message.resolution?.length && this.resolutionPreview) {
                this.resolutionPreview.name = message.resolution[0];
                this.setDirtyCanvas(true, true);
            }
        };
    },
});
