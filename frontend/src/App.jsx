import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState(null);
  const [classificationModel, setClassificationModel] = useState('phoBert');
  const [summaryModel, setSummaryModel] = useState('vit5');

  const handlePhoBertSubmit = async (event) => {
  event.preventDefault();

  //  Kiểm tra nếu không phải là URL thì không cho gửi
  if (!/^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/.test(message)) {
    alert("Vui lòng nhập một đường link hợp lệ để hệ thống phân tích.");
    return;
  }

  let res;
  try {
    const requestBody = {
      text: message,
      summary_model: summaryModel
    };

    //  Luôn dùng API xử lý link
    res = await fetch(`/api/v1/predict/withlink/${classificationModel}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    });

    const data = await res.json();
    let label = "Giả";
    if (data.data.label.label === 1) label = "Thật";

    if (data.success) {
      setResponse({
        label: label,
        summary: data.data.summary || 'Chưa có tóm tắt',
        links: data.data.links || []
      });
    } else {
      setResponse({ label: 'Lỗi: ' + data.message, summary: '', links: [] });
    }

  } catch (err) {
    setResponse({ label: 'Lỗi kết nối đến server', summary: '', links: [] });
  }
};

  return (
    <div className="wrapper">
      <div className="chat-container">
        <div className="header">
          <i className="fas fa-robot"></i> Hệ thống phản hồi thông tin về tin tức
        </div>

        <div className="chat-box">
          {response ? (
            <>
              <div className="message user">Yêu cầu: "{message}"</div>

              <div className="message bot">
                <i className="fas fa-circle-exclamation text-danger"></i> {response.label}
              </div>

              <div className="message bot">
                <i className="fas fa-file-alt text-primary"></i> Tóm tắt: {response.summary}
              </div>

              <div className="message bot">
                <i className="fas fa-link text-success"></i> Những đường link liên quan:
              </div>

              {response.links.map((link, idx) => (
                <div className="message bot" key={idx}>
                  <a href={link} target="_blank" rel="noopener noreferrer">Link {link}</a>
                </div>
              ))}
            </>
          ) : (
            <div className="message bot">Chưa có kết quả nào...</div>
          )}
        </div>

        <form className="input-box mt-3" onSubmit={handlePhoBertSubmit}>
          <input
            type="text"
            name="message"
            className="form-control mb-2"
            placeholder="Nhập nội dung hoặc đường link..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
          />

          <label htmlFor="model_classification">Chọn mô hình phân lớp</label>
          <select
            className="form-select mb-2"
            id="model_classification"
            value={classificationModel}
            onChange={(e) => setClassificationModel(e.target.value)}
          >
            <option value="bilstm">BiLSTM</option>
            <option value="phoBert">PhoBERT</option>
            <option value="roberta">RoBERTa</option>
          </select>

          <label htmlFor="model_summary">Chọn mô hình tóm tắt</label>
          <select
            className="form-select mb-2"
            id="model_summary"
            value={summaryModel}
            onChange={(e) => setSummaryModel(e.target.value)}
          >
            <option value="vit5">ViT5</option>
            <option value="bartpho">BARTPho</option>
            <option value="mT5">mT5</option>
            {/* <option value="phobert">... (sau này thêm nếu cần) */}
          </select>

          <button type="submit" className="btn btn-success mt-2 w-100">
            <i className="fas fa-paper-plane"></i> Gửi yêu cầu
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
