from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers.invoice_router import invoice_router
from app.core.settings import settings


def create_application() -> FastAPI:
    application = FastAPI(
        title="StoneHub OCR API",
        description="OCR API for Vietnamese invoices powered by Gemini.",
        version="1.0.0",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_origin_regex=settings.cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(invoice_router, prefix="/api/v1/invoices", tags=["invoices"])
    return application


app = create_application()
