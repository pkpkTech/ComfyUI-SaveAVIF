import { app } from "../../scripts/app.js";
import { applyTextReplacements } from "../../scripts/utils.js";

app.registerExtension({
	name: "pkpk.saveavif.exoutput",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "SaveAvif") {
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
				const widget = this.widgets.find((w) => w.name === "filename_prefix");
				widget.serializeValue = () => {
					return applyTextReplacements(app, widget.value);
				};

				return r;
			};
		} else {
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
				if (!this.properties || !("Node name for S&R" in this.properties)) {
					this.addProperty("Node name for S&R", this.constructor.type, "string");
				}

				return r;
			};
		}
	},
});
