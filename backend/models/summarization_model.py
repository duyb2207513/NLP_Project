import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import gdown
import os

# ViT5 model folder from Google Drive
vit5_folder_id = "17VPwg5vNLqhibd9dMWuf47vQ1NSr4MwG"  # Correct Google Drive folder ID
vit5_local_path = "vit5_summarization_have_evaluation"  # Local folder name




# Download folder from Google Drive if it doesn't exist
if not os.path.exists(vit5_local_path):
    try:
        gdown.download_folder(
            id=vit5_folder_id,
            output=vit5_local_path,
            quiet=False,
            use_cookies=False
        )
        print(f"Downloaded and extracted to '{vit5_local_path}'.")
    except Exception as e:
        print(f"Failed to download folder: {e}. Please check permissions or download manually from https://drive.google.com/drive/folders/{vit5_folder_id}")
else:
    print(f"Folder '{vit5_local_path}' already exists, skipping download.")

# Load tokenizer and model from the local folder

vit5_tokenizer = AutoTokenizer.from_pretrained(vit5_local_path)
vit5_model = AutoModelForSeq2SeqLM.from_pretrained(vit5_local_path)

    




# file_id = "13mXjBvICSBKDX5_eUqYbL7m0DBSu86ZW"
# output = "bilstm_fakenews_model.pth"
import os
import gdown
import zipfile
# https://drive.google.com/file/d/141uyhqk-hqDGeDUe4W6E9vgBGP4qvhzq/view?usp=drive_link
bartpho_id = "141uyhqk-hqDGeDUe4W6E9vgBGP4qvhzq"
bartpho_local_path = "bartpho_fakenews_model"
output = "bartpho_fakenews_model.zip"
if not os.path.exists(bartpho_local_path):
    url = f"https://drive.google.com/uc?id={bartpho_id}"
    gdown.download(url, output, quiet=False)
    with zipfile.ZipFile("bartpho_fakenews_model.zip", 'r') as zip_ref:
        zip_ref.extractall("bartpho_fakenews_model")
    os.remove(output)
else:
    print(f"File {output} đã tồn tại, bỏ qua tải lại.")
    
bartpho_tokenizer = AutoTokenizer.from_pretrained(f"{bartpho_local_path}/bartpho_summarization")
bartpho_model = AutoModelForSeq2SeqLM.from_pretrained(f"{bartpho_local_path}/bartpho_summarization")

summarization_models = {
    "vit5": {
        "tokenizer": vit5_tokenizer,
        "model": vit5_model
    },
    "bartpho": {
        "tokenizer": bartpho_tokenizer,
        "model": bartpho_model
    }
}
