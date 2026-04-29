import zipfile
import json
import os
import shutil

def remove_buggy_key(d):
    if isinstance(d, dict):
        if "quantization_config" in d:
            del d["quantization_config"]
        for v in d.values():
            remove_buggy_key(v)
    elif isinstance(d, list):
        for item in d:
            remove_buggy_key(item)

print("Unzipping model...")
with zipfile.ZipFile("trained_plant_disease_model.keras", "r") as z:
    z.extractall("temp_model")

print("Fixing the JSON configuration...")
with open("temp_model/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

remove_buggy_key(config)

with open("temp_model/config.json", "w", encoding="utf-8") as f:
    json.dump(config, f)

print("Re-zipping into a fixed model file...")
with zipfile.ZipFile("fixed_plant_disease_model.keras", "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk("temp_model"):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, "temp_model")
            z.write(file_path, arcname)

shutil.rmtree("temp_model")
print("Success! Saved as 'fixed_plant_disease_model.keras'")