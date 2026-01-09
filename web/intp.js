import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "LumyLogic.INTPlus",
    
    async nodeCreated(node) {
        if (node.comfyClass !== "INTPlus") return;
        
        // Find the int widget
        const intWidget = node.widgets?.find(w => w.name === "int");
        if (!intWidget) return;
        
        // Find the control_mode widget to handle initial randomization
        const controlWidget = node.widgets?.find(w => w.name === "control_mode");
        if (controlWidget) {
            const origCallback = controlWidget.callback;
            controlWidget.callback = function(value) {
                if (origCallback) origCallback.call(this, value);
                // If random_seed selected and value is 0 or less, randomize immediately
                if (value === "random_seed" && intWidget.value <= 0) {
                    intWidget.value = Math.floor(Math.random() * 1115899906842624) + 1;
                    if (app.graph) {
                        app.graph.setDirtyCanvas(true, true);
                    }
                }
            };
        }
        
        // Store original onExecuted if exists
        const origOnExecuted = node.onExecuted;
        
        node.onExecuted = function(message) {
            // Call original if exists
            if (origOnExecuted) {
                origOnExecuted.apply(this, arguments);
            }
            
            // Update widget with value from backend
            const newValue = message?.value?.[0];
            if (newValue !== undefined) {
                intWidget.value = newValue;
                if (app.graph) {
                    app.graph.setDirtyCanvas(true, true);
                }
            }
        };
    },
});
