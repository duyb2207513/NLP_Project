# Thực thi backend

## Yêu cầu hệ thống

- Python 3.8+

---

## Cách chạy backend Flask

### 1. Vào thư mục backend
```bash
cd backend
```

### 2. (Khuyến nghị) Tạo virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Trên Linux/macOS
# .\venv\Scripts\activate  # Trên Windows

```

### 3. Cài đặt thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng Flask
```bash
python3 app.py
```

Nếu app không khởi chạy, hãy thử thêm dòng sau vào cuối file app.py:
```python
if __name__ == "__main__":
    app.run(debug=True)
```

Mặc định Flask chạy tại địa chỉ 
```bash
http://127.0.0.1:5000/
```
