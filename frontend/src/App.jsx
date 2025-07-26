import { useState} from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState(null);
  const [classificationModel, setClassificationModel] = useState('phoBert');
  const [summaryModel, setSummaryModel] = useState('vit5');
  const [changes,setchanges]= useState(null);
  // const [retry, setRetry] = useState(false);
  const handleReset = () => {
    setMessage('');
    setResponse(null);
  };
 

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
      console.log('Data from API:', data); 
      setResponse({
        label: label,
        summary: data.data.summary || 'Chưa có tóm tắt',
        links: data.data.links || []
      });
    } else {
      setResponse({ label: 'Lỗi: ' + data.message, summary: '', links: [] });
    }

  } catch (err) {
    console.log(err)
    setResponse({ label: 'Lỗi kết nối đến server', summary: '', links: [] });
  }
    setchanges('no');
};

  return (
    <div >
    <div className="header text-primary" >
          <i className="fas fa-robot"></i> Hệ thống phản hồi thông tin về tin tức
        </div>  
      {changes ? (
        <div className="chat-container  ">
       
        <form className="d-flex input-box mt-3 bg-light m-5 border-2 p-5  " onSubmit={handlePhoBertSubmit}>
        <div className="w-50 mx-2 ">
            
        <div  >
          <div className="model w-100">
            <label htmlFor="model_classification"><b>Mô hình phân lớp</b></label>
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
           
          </div>

          <div className="model w-100">
            <label htmlFor="model_summary"><b>Mô hình tóm tắt</b></label>
            <select
              className="form-select mb-2"
              id="model_summary"
              value={summaryModel}
              onChange={(e) => setSummaryModel(e.target.value)}
            >
              {/* <option selected>Vui lòng chọn mô hình phân lớp</option> */}
              <option value="vit5">ViT5</option>
              <option value="bartpho">BARTPho</option>
              <option value="mT5">mT5</option>
              {/* <option value="phobert">... (sau này thêm nếu cần) */}
            </select>
          </div>
           <input
            type="text"
            name="message"
            className="form-control "
            placeholder="Nhập nội dung hoặc đường link..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
          />
           <button   type="submit" className="btn btn-secondary w-100">
            <i className="fas fa-paper-plane"></i> Gửi yêu cầu
          </button>
        </div>
        </div>
             
        <div className="w-50  ">
          {response ? (
            <div className='cover-chatbox '>


              <div className="chat-box">
                

                <div className="message bot">
                  <p className="label-message"><i class="fa-regular fa-circle-check text-success"></i> <b>{response.label}</b></p> 
                </div>

                <div className="message bot">
                  <i className="fas fa-file-alt text-primary"></i> <b>Tóm tắt:</b> {response.summary}
                </div>

                <div className="message bot">
                  <i className="fas fa-link text-success"></i> <b>Những đường dẫn liên quan:</b>
                </div>

                {response.links.length != 0 ? (response.links.map((link)=> (
                  <div className="message bot" key={link}>
                    <a href={link} target="_blank" rel="noopener noreferrer">Link {link}</a>
                  </div>
                )))
                :<p>Không có</p>}

              </div>
             

            </div>
          ) : (
            <div className='input-text'>

            <input
            type="text"
            name="message"
            className="form-control "
            placeholder="Nhập nội dung hoặc đường link..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
          />

            
            <button type="submit" className="btn btn-secondary w-25">
            <i className="fas fa-paper-plane"></i> Gửi yêu cầu
          </button>

            </div>
          )}
          
      
        </div>
        
        </form>
        
      </div>
      ):(
        <div className="wrapper">

          <div className="chat-container  ">
        
        <form className="input-box mt-3 bg-light m-5 border-2 p-5  " onSubmit={handlePhoBertSubmit}>
       
        <div className="chosen-model">
          <div className="model w-50">
            <label htmlFor="model_classification"><b>Mô hình phân lớp</b></label>
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
          </div>

          <div className="model w-50">
            <label htmlFor="model_summary"><b>Mô hình tóm tắt</b></label>
            <select
              className="form-select mb-2"
              id="model_summary"
              value={summaryModel}
              onChange={(e) => setSummaryModel(e.target.value)}
            >
              {/* <option selected>Vui lòng chọn mô hình phân lớp</option> */}
              <option value="vit5">ViT5</option>
              <option value="bartpho">BARTPho</option>
              <option value="mT5">mT5</option>
              {/* <option value="phobert">... (sau này thêm nếu cần) */}
            </select>
          </div>
        </div>
          

          
        <div >
          {response ? (
            <div className='cover-chatbox'>


              <div className="chat-box">
                <div className="message user">Yêu cầu: "{message}"</div>

                <div className="message bot">
                  <b className="label-message"> {response.label}</b> 
                </div>

                <div className="message bot">
                  <i className="fas fa-file-alt text-primary"></i> <b>Tóm tắt:</b> {response.summary}
                </div>

                <div className="message bot">
                  <i className="fas fa-link text-success"></i> <b>Những đường link liên quan:</b>
                </div>
                {response.links}
                {response.links.map((link, idx) => (
                  <div className="message bot" key={idx}>
                    <a href={link} target="_blank" rel="noopener noreferrer">Link {link}</a>
                  </div>
                ))}
              
                

              </div>
                <button onClick={handleReset} type="button" className="btn btn-secondary w-100">
                  <i className="fas fa-paper-plane"></i> Chạy lại
                  </button>

            </div>
          ) : (
            <div className='input-text'>

            <input
            type="text"
            name="message"
            className="form-control "
            placeholder="Nhập nội dung hoặc đường link..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
          />
            <button   type="submit" className="btn btn-secondary w-25">
            <i className="fas fa-paper-plane"></i> Gửi yêu cầu
          </button>

            </div>
          )}
          
      
        </div>
        
        </form>
        
      </div>

        </div>
      )}
    </div>
  );
}

export default App;
