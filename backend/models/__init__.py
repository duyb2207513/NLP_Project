import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import gdown
import zipfile
import os

# roberta_path = "https://drive.google.com/file/d/1x49rDCKdmclDXR1RXm2AnmLuFopqnFxc/view?usp=drive_link"

# # Dùng đúng model đã huấn luyện
# roberta = "xlm-roberta-base"

# # Load tokenizer
# roberta_tokenizer = AutoTokenizer.from_pretrained(roberta)

# # Khởi tạo lại model đúng kiến trúc
# roberta_model = AutoModelForSequenceClassification.from_pretrained(roberta, num_labels=2)


# # Load trọng số từ file đã lưu
# roberta_model.load_state_dict(torch.load("models/roberta_fakenews.pth", map_location=torch.device("cpu")))
# roberta_model.eval()

# PhoBERT pretrained model
phoBert = "vinai/phobert-base"

phoBert_id = "1V1UaOMhAqSfag1qtuAE0IA8WGaVBZ6LK"

output = "phobert_fakenews_model.pth"
if not os.path.exists(output):
    url = f"https://drive.google.com/uc?id={phoBert_id}"
    gdown.download(url, output, quiet=False)
else:
    print(f"File {output} đã tồn tại, bỏ qua tải lại.")

# Load tokenizer
phoBert_tokenizer = AutoTokenizer.from_pretrained(phoBert)

# Khởi tạo model với đúng kiến trúc
phoBert_model = AutoModelForSequenceClassification.from_pretrained(phoBert, num_labels=2)

# Load trọng số đã train
phoBert_model.load_state_dict(torch.load("phobert_fakenews_model.pth", map_location=torch.device("cpu")))
phoBert_model.eval()

# class BiLSTMClassifier(nn.Module):
#     def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, padding_idx):
#         super(BiLSTMClassifier, self).__init__()
#         self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=padding_idx)
#         self.lstm = nn.LSTM(embedding_dim, hidden_dim, bidirectional=True, batch_first=True)
#         self.dropout = nn.Dropout(0.5)
#         self.fc = nn.Linear(hidden_dim * 2, output_dim)
    
#     def forward(self, x):
#         embedded = self.embedding(x)
#         lstm_out, _ = self.lstm(embedded)
#         # Lấy hidden state cuối cùng
#         out = lstm_out[:, -1, :]
#         out = self.dropout(out)
#         logits = self.fc(out)
#         return torch.sigmoid(logits)

# # Tham số mô hình (phải khớp với lúc train)
# vocab_size = len(phoBert_tokenizer.word_index) + 1  # Dùng word_index của Keras nếu muốn tái sử dụng từ điển
# embedding_dim = 100
# hidden_dim = 64
# output_dim = 1
# padding_idx = 0  # padding index (0 nếu dùng pad_sequences)

# # Khởi tạo mô hình
# bilstm_model = BiLSTMClassifier(vocab_size, embedding_dim, hidden_dim, output_dim, padding_idx)

# # Load trọng số từ file .pth
# bilstm_model.load_state_dict(torch.load("models/Bi-LSTM_fakenews.pth", map_location=torch.device('cpu')))
# bilstm_model.eval()