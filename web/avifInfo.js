import { app } from "/scripts/app.js";
app.registerExtension({
	name: "pkpk.saveavif.prompt",
setup(app,file){

async function getAvifExifData(avifFile) {
	const reader = new FileReader();
	reader.readAsArrayBuffer(avifFile);
  
	return new Promise((resolve, reject) => {
	  reader.onloadend = function() {
		const buffer = reader.result;
		const view = new DataView(buffer);
		let offset = 0;
  
		// Search for the "EXIF" or "Exif" tag
		while (offset < view.byteLength - 4) {
		  const tag = view.getUint32(offset, true);
		  if (tag === 0x46495845 || tag === 0x66697845) {
			const exifOffset = offset + 6; 
			const exifData = buffer.slice(exifOffset);
			const exifString = new TextDecoder().decode(exifData).replaceAll(String.fromCharCode(0), '');
			let exifJsonString = exifString.slice(exifString.indexOf("Workflow"));
			let promptregex="(?<!\{)}Prompt:{(?![\w\s]*[\}])";
			let exifJsonStringMap = new Map([
				["workflow",exifJsonString.slice(9,exifJsonString.search(promptregex)+1)],
				["prompt",exifJsonString.substring((exifJsonString.search(promptregex)+8))]
			]);
			let fullJson=Object.fromEntries(exifJsonStringMap);
			
			resolve(fullJson);
			
		  }
		  offset++;
		}
		
		reject(new Error('EXIF metadata not found'));
}})};
	


const handleFile = app.handleFile;
app.handleFile = async function(file) {
	if (file.type === "image/avif") {
		
		const avifInfo =await getAvifExifData(file);
		if (avifInfo) {
			if (avifInfo.workflow) {
				if(app.load_workflow_with_components) {
					app.load_workflow_with_components(avifInfo.workflow);
				}
				else
					this.loadGraphData(JSON.parse(avifInfo.workflow));
			}
		}
	} else {
		return handleFile.apply(this, arguments);
	}
}

},});
