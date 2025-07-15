import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification,AutoModelForSeq2SeqLM
import torch
import gdown
import zipfile
import os
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# PhoBERT pretrained model
roberta_id = "1GgfQ0u-lTcywm4gY8pak-OBzxEDLIu9R"
roberta_link = "roberta_fakenews_model"
output = "roberta_fakenews_model.zip"
if not os.path.exists(roberta_link):
    url = f"https://drive.google.com/uc?id={roberta_id}"
    gdown.download(url, output, quiet=False)
    with zipfile.ZipFile("roberta_fakenews_model.zip", 'r') as zip_ref:
        zip_ref.extractall("roberta_fakenews_model")
    os.remove(output)
else:
    print(f"File {output} đã tồn tại, bỏ qua tải lại.")
    
# Load tokenizer
roberta_tokenizer = AutoTokenizer.from_pretrained("./roberta_fakenews_model/roberta_fakenews_model")

# Khởi tạo model với đúng kiến trúc
roberta_model = AutoModelForSequenceClassification.from_pretrained("./roberta_fakenews_model/roberta_fakenews_model", num_labels=2)


# PhoBERT pretrained model
phoBert_id = "1vYhSu-Kw2hnATrnQR3k7TQ2lLkIysXCT"
phoBert_link = "phobert_fakenews_model"
output = "phobert_fakenews_model.zip"
if not os.path.exists(phoBert_link):
    url = f"https://drive.google.com/uc?id={phoBert_id}"
    gdown.download(url, output, quiet=False)
    with zipfile.ZipFile("phobert_fakenews_model.zip", 'r') as zip_ref:
        zip_ref.extractall("phobert_fakenews_model")
    os.remove(output)
else:
    print(f"File {output} đã tồn tại, bỏ qua tải lại.")
    
# Load tokenizer
phoBert_tokenizer = AutoTokenizer.from_pretrained("./phobert_fakenews_model/phobert_fakenews_model")

# Khởi tạo model với đúng kiến trúc
phoBert_model = AutoModelForSequenceClassification.from_pretrained("./phobert_fakenews_model/phobert_fakenews_model", num_labels=2)

# Load trọng số đã train

bilstm_tokenizer = Tokenizer(num_words=None, oov_token="<unk>")
word_index = bilstm_tokenizer.word_index

class BiLSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, padding_idx):
        super(BiLSTMClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=padding_idx)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, bidirectional=True, batch_first=True)
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
    
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        # Lấy hidden state cuối cùng
        out = lstm_out[:, -1, :]
        out = self.dropout(out)
        logits = self.fc(out)
        return torch.sigmoid(logits)

# Tham số mô hình (phải khớp với lúc train)
vocab_size = len(word_index) + 1  # Dùng word_index của Keras nếu muốn tái sử dụng từ điển
embedding_dim = 300
hidden_dim = 256
output_dim = 1
padding_idx = 0  # padding index (0 nếu dùng pad_sequences)
bilstm_link = "models/Bi-LSTM_fakenews_model.pth"

# Khởi tạo mô hình
bilstm_model = BiLSTMClassifier(vocab_size, embedding_dim, hidden_dim, output_dim, padding_idx)

# Load trọng số từ file .pth
# 1. Tải checkpoint
checkpoint = torch.load(bilstm_link, map_location=torch.device('cpu'))

# 2. Chỉ load state_dict của model
state_dict = checkpoint.get('model_state_dict', checkpoint.get('state_dict', checkpoint))
bilstm_model.load_state_dict(state_dict, strict=False)

# 3. Chuyển sang chế độ eval
bilstm_model.eval()


tokenize_sumary = AutoTokenizer.from_pretrained("VietAI/vit5-base-vietnews-summarization")
model_sumary = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base-vietnews-summarization")

