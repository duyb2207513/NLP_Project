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
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, dropout):
        super(BiLSTMClassifier, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)

        self.lstm1 = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(hidden_dim * 2, hidden_dim, batch_first=True, bidirectional=True)
        self.lstm3 = nn.LSTM(hidden_dim * 2, hidden_dim, batch_first=True, bidirectional=True)

        self.attention = nn.Linear(hidden_dim * 2, 1)

        self.dropout = nn.Dropout(dropout)

        self.fc1 = nn.Linear(hidden_dim * 2, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.fc3 = nn.Linear(64, output_dim)

        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        embedded = self.embedding(x)                      # (batch, seq_len, embedding_dim)
        lstm_out1, _ = self.lstm1(embedded)               # (batch, seq_len, hidden_dim*2)
        lstm_out2, _ = self.lstm2(lstm_out1)              # (batch, seq_len, hidden_dim*2)
        lstm_out3, _ = self.lstm3(lstm_out2)              # (batch, seq_len, hidden_dim*2)

        # Attention cơ bản: trọng số theo thời gian
        attn_weights = torch.softmax(self.attention(lstm_out3), dim=1)   # (batch, seq_len, 1)
        context = torch.sum(attn_weights * lstm_out3, dim=1)             # (batch, hidden_dim*2)

        out = self.dropout(context)
        out = self.relu(self.bn1(self.fc1(out)))          # (batch, 128)
        out = self.relu(self.bn2(self.fc2(out)))          # (batch, 64)
        out = self.fc3(out)                               # (batch, 1)
        return self.sigmoid(out)  # giữ shape (batch_size, 1)


# Tham số mô hình (phải khớp với lúc train)



# biLSTM pretrained model

# ID của file từ link Google Drive

file_id = "13mXjBvICSBKDX5_eUqYbL7m0DBSu86ZW"
output = "bilstm_fakenews_model.pth"

if not os.path.exists(output):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)
else:
    print(f"File {output} đã tồn tại, bỏ qua tải lại.")

# Load trọng số từ file .pth
# 1. Tải checkpoint
checkpoint = torch.load(output, map_location="cpu")
config = checkpoint['model_config']

# Khởi tạo mô hình
bilstm_model =  BiLSTMClassifier(
    vocab_size=config['vocab_size'],
    embedding_dim=100, # Corrected embedding_dim
    hidden_dim=64,     # Corrected hidden_dim
    output_dim=config['output_dim'],
    dropout=config['dropout']
)

# 2. # Load trạng thái
# state_dict = checkpoint.get('model_state_dict', checkpoint.get('state_dict', checkpoint))
bilstm_model.load_state_dict(checkpoint['model_state_dict'])

# 3. Chuyển sang chế độ eval
bilstm_model.eval()


tokenize_sumary = AutoTokenizer.from_pretrained("VietAI/vit5-base-vietnews-summarization")
model_sumary = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base-vietnews-summarization")

