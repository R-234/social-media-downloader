import zipfile
import os
import json
from datetime import datetime

# -------------------------------
# ZIP FUNCTION
# -------------------------------
def create_zip(folder_path, zip_name="downloads.zip"):
    zip_path = os.path.join(folder_path, zip_name)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file != zip_name:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=file)

    return zip_path

# -------------------------------
# DATABASE FUNCTION
# -------------------------------
DB_FILE = "database.json"

def save_to_db(filename, url, platform):
    data = []

    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)

    data.append({
        "file": filename,
        "url": url,
        "platform": platform,
        "time": str(datetime.now())
    })

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)