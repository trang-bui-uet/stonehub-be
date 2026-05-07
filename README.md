## StoneHub BE - Gemini OCR API

### 1) Cài đặt

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Cấu hình môi trường

- Copy file `.env.example` thành `.env`
- Điền `GEMINI_API_KEY` lấy từ [Google AI Studio](https://aistudio.google.com/app/apikey)
- Nếu cần đổi model, chỉnh `GEMINI_MODEL` (`gemini-2.5-flash` hoặc `gemini-2.5-flash-lite`)

### 3) Chạy server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4) API cho FE

- Endpoint: `POST /api/v1/invoices/extract`
- Content type: `multipart/form-data`
- Field upload: `image`

Response mẫu:

```json
{
  "status": "success",
  "data": {
    "organization_name": "Công ty ABC",
    "tax_code": "0312345678",
    "address": "123 Đường XYZ, Quận 1, TP.HCM",
    "legal_representative": null,
    "phone_number": null,
    "email": null,
    "raw_text": "{...json từ Gemini...}"
  }
}
```
