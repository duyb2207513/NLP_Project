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

summarization_models = {
    "vit5": {
        "tokenizer": vit5_tokenizer,
        "model": vit5_model
    },
    # "bart": {
    #     "tokenizer": bart_tokenizer,
    #     "model": bart_model
    # }
}
# vit5_model.eval()  # Set to inference mode

# # # Function to summarize text
# def summarize_text(text, max_length=50, num_beams=2):
#     inputs = vit5_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
#     summary_ids = vit5_model.generate(**inputs, max_length=max_length, num_beams=num_beams)
#     summary = vit5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Test the function
# if __name__ == "__main__":
#     sample_text = """
# Các doanh nghiệp dưới đây cho thấy xu hướng "xanh hóa" không chỉ là lựa chọn bắt kịp thời đại, mà còn là động lực đổi mới toàn diện chuỗi giá trị nông nghiệp.

# Năm 2013, Nguyễn Tính bắt đầu tiếp quản mô hình hộ kinh doanh nuôi thủy sản của gia đình tại Đồng Tháp. Suốt 10 năm gắn bó với nghề, anh chứng kiến không ít bất cập, đặc biệt là tình trạng lạm dụng kháng sinh trong chăn nuôi, ảnh hưởng đến chất lượng thủy sản và môi trường. Trăn trở với điều đó, anh âm thầm tìm kiếm một hướng đi khác biệt, bền vững hơn.

# Đến năm 2023, sau nhiều năm tích lũy kinh nghiệm và tự nghiên cứu, Tính cùng các cộng sự chính thức thành lập Alpha Amin, với mục tiêu phát triển giải pháp phòng bệnh cho cá rô phi không dùng kháng sinh. Giai đoạn đầu, nhóm sáng lập vừa đảm nhiệm phần kỹ thuật, vừa trực tiếp thử nghiệm sản phẩm tại các hộ nuôi nhỏ lẻ trong tỉnh, từng bước hoàn thiện quy trình trước khi mở rộng quy mô.
# """
# summary = summarize_text(sample_text)
# print("Tóm tắt:", summary)