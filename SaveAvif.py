import numpy as np
from PIL import Image
import pillow_avif
import folder_paths
import os
import json

from comfy.cli_args import args

class SaveAvif:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"images": ("IMAGE", ),
                    "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                    "c_quality":("INT", {"default": 75, "min": 0, "max": 100, "step": 1}),
                    "enc_speed":("INT", {"default": 6, "min": 0, "max": 10, "step": 1})},
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image( pass-through )",)
    FUNCTION = "save_avif"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def save_avif(self, images, filename_prefix="ComfyUI", c_quality=75, enc_speed=6, prompt=None, extra_pnginfo=None):

        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            img_exif = img.getexif()

            if not args.disable_metadata:
                if prompt is not None:
                    prompt_text = "".join(json.dumps(prompt))
                    img_exif[0x010f] ="Prompt:" + prompt_text
                if extra_pnginfo is not None:
                    workflow_metadata = str()
                    for x in extra_pnginfo:
                        workflow_metadata += "".join(json.dumps(extra_pnginfo[x]))
                    img_exif[0x010e] = "Workflow:"+ workflow_metadata
            
            file = f"{filename}_{counter:05}_.avif"
            img.save(os.path.join(full_output_folder, file), quality= c_quality, speed= enc_speed, exif= img_exif)
            
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            });
            counter += 1

        return { "result": (images,), "ui": { "images": results } }
        
NODE_CLASS_MAPPINGS = {
    "SaveAvif": SaveAvif
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveAvif": "Save AVIF"
}

