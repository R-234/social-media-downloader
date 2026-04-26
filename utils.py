import zipfile
import os
import json
from datetime import datetime

DB_FILE = "database.json"

def create_zip(folder_path, zip_name="downloads.zip"):
    zip_path = os.path.join(folder_path, zip_name)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file == zip_name:
                    continue
                fp = os.path.join(root, file)
                zipf.write(fp, arcname=file)
    return zip_path

def save_to_db(filename, url, platform):
    data = []
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            data = []

    data.append({
        "file": filename,
        "url": url,
        "platform": platform,
        "time": datetime.now().isoformat(timespec="seconds"),
    })

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)