from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.invoice_ocr_model import InvoiceOcrResponse
from app.services.gemini_ocr_service import extract_invoice_with_gemini

invoice_router = APIRouter()


@invoice_router.post("/extract", response_model=InvoiceOcrResponse)
async def extract_invoice(image: UploadFile = File(...)) -> InvoiceOcrResponse:
    if image.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên file không hợp lệ.",
        )
    image_bytes = await image.read()
    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File ảnh rỗng.",
        )
    try:
        data = extract_invoice_with_gemini(image_bytes)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Không thể xử lý OCR từ Gemini: {error}",
        ) from error
    return InvoiceOcrResponse(status="success", data=data)
