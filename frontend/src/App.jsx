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
           <button   type="submit" className=" mt-5 btn btn-secondary w-100">
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
        <div className="wrapper ">

          <div className="chat-container-layout1 bg-white ">
        
        <form className="align-items-center gap-2 p-3" onSubmit={handlePhoBertSubmit}>
  

  {/* Ô nhập nội dung hoặc link */}
  <input
    type="text"
    name="message"
    className=" form-input"
    placeholder="Nhập nội dung hoặc đường link..."
    value={message}
    onChange={(e) => setMessage(e.target.value)}
    required
  />
  <div className=' d-flex justify-content-lg-between'>
    {/* Dropdown chọn mô hình phân lớp */}
    <div className='d-flex'>
  
      <select
      className="px-2 mx-2 form-select-sm "
      value={classificationModel}
      onChange={(e) => setClassificationModel(e.target.value)}
    >
      <option value="bilstm">BiLSTM</option>
      <option value="phoBert">PhoBERT</option>
      <option value="roberta">RoBERTa</option>
    </select>

    {/* Dropdown chọn mô hình tóm tắt */}

    <select
      className="px-2 mx-2 form-select-sm"
      value={summaryModel}
      onChange={(e) => setSummaryModel(e.target.value)}
    >
      <option value="vit5">ViT5</option>
      <option value="bartpho">BARTPho</option>
      <option value="mT5">mT5</option>
    </select>
    </div>
    {/* Nút gửi */}
    <button type="submit" className="btn btn-secondary">
      <i className="fas fa-paper-plane"></i>
    </button>
  </div>

  
        </form>

      </div>

        </div>
      )}
    </div>
  );
}

export default App;
