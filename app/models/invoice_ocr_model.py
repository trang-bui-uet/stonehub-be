from pydantic import BaseModel, Field


class InvoiceOcrData(BaseModel):
    organization_name: str | None = Field(default=None)
    tax_code: str | None = Field(default=None)
    address: str | None = Field(default=None)
    legal_representative: str | None = Field(default=None)
    phone_number: str | None = Field(default=None)
    email: str | None = Field(default=None)
    raw_text: str = Field(default="")


class InvoiceOcrResponse(BaseModel):
    status: str
    data: InvoiceOcrData
