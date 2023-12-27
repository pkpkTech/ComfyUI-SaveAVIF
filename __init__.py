import shutil
import folder_paths
import os, sys, subprocess
import filecmp



print("### Loading: Save AVIF")

comfy_path = os.path.dirname(folder_paths.__file__)

def setup_js():
   self_path = os.path.dirname(__file__)
   js_dest_path = os.path.join(comfy_path, "web", "extensions", "saveavif")
   info_src_path = os.path.join(self_path, "web", "avifInfo.js")
   sex_src_path = os.path.join(self_path, "web", "saveAvifExtraOutput.js")
     
   ## Creating folder if it's not present, then Copy. 
   print("Copying JS files for Workflow loading")
   if (os.path.isdir(js_dest_path)==False):
     os.mkdir(js_dest_path)
   
   shutil.copy(info_src_path, js_dest_path)
   shutil.copy(sex_src_path, js_dest_path)

setup_js()

from .SaveAvif import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']