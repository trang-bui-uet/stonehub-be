import json
from io import BytesIO

from PIL import Image, UnidentifiedImageError
import google.generativeai as genai

from app.core.settings import settings
from app.models.invoice_ocr_model import InvoiceOcrData

OCR_PROMPT = """Bạn là chuyên gia trích xuất thông tin hóa đơn, phiếu thu, giấy tờ kinh doanh Việt Nam.
Hãy trích xuất chính xác các thông tin sau từ ảnh và trả về đúng định dạng JSON:
{
  "organization_name": "Tên công ty / doanh nghiệp",
  "tax_code": "Mã số thuế",
  "address": "Địa chỉ đầy đủ",
  "legal_representative": "Người đại diện / Giám đốc (nếu có)",
  "phone_number": "Số điện thoại (nếu có)",
  "email": "Email (nếu có)"
}
Quy tắc:
- Chỉ trích xuất thông tin có thật trong ảnh, không đoán.
- Nếu không tìm thấy trường nào thì để null.
- Giữ nguyên dấu tiếng Việt, không thêm thắt.
- Chỉ trả JSON, không bao bọc markdown.
"""
DEFAULT_OCR_DATA = InvoiceOcrData()

genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel(settings.gemini_model)


def extract_invoice_with_gemini(image_bytes: bytes) -> InvoiceOcrData:
    image = _load_image_from_bytes(image_bytes)
    response = model.generate_content([OCR_PROMPT, image])
    raw_text = _extract_response_text(response)
    parsed_content = _parse_json_content(raw_text)
    if not isinstance(parsed_content, dict):
        return DEFAULT_OCR_DATA.model_copy(update={"raw_text": raw_text})
    normalized_content = {
        "organization_name": _resolve_string_value(parsed_content.get("organization_name")),
        "tax_code": _resolve_string_value(parsed_content.get("tax_code")),
        "address": _resolve_string_value(parsed_content.get("address")),
        "legal_representative": _resolve_string_value(parsed_content.get("legal_representative")),
        "phone_number": _resolve_string_value(parsed_content.get("phone_number")),
        "email": _resolve_string_value(parsed_content.get("email")),
        "raw_text": raw_text,
    }
    return InvoiceOcrData(**normalized_content)


def _load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    try:
        return Image.open(BytesIO(image_bytes))
    except UnidentifiedImageError as error:
        raise ValueError("File tải lên không phải ảnh hợp lệ.") from error


def _extract_response_text(response: object) -> str:
    response_text = getattr(response, "text", None)
    if isinstance(response_text, str):
        return response_text.strip()
    return ""


def _parse_json_content(raw_text: str) -> dict | None:
    if raw_text == "":
        return None
    sanitized_text = _sanitize_markdown_json(raw_text)
    try:
        return json.loads(sanitized_text)
    except json.JSONDecodeError:
        return None


def _sanitize_markdown_json(raw_text: str) -> str:
    if not raw_text.startswith("```"):
        return raw_text
    stripped_text = raw_text.strip().strip("`")
    if stripped_text.startswith("json"):
        return stripped_text[4:].strip()
    return stripped_text.strip()


def _resolve_string_value(input_value: object) -> str | None:
    if isinstance(input_value, str):
        trimmed_value = input_value.strip()
        if trimmed_value == "":
            return None
        return trimmed_value
    return None
