from typing import Optional
from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=4000)
    terms: str = Field(..., min_length=2, max_length=12000)
    effective_date: str = Field(..., min_length=2, max_length=100)
    additional_instructions: Optional[str] = Field(default="", max_length=5000)

    @field_validator("document_type", "parties", "terms", "effective_date", "additional_instructions", mode="before")
    @classmethod
    def strip_values(cls, value):
        if value is None:
            return ""
        return str(value).strip()


class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str
    demo_mode: bool
    disclaimer: str
