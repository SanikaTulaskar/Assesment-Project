from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    location: str

class Company(BaseModel):
    company_id: int
    name: str
    location: str

    class Config:
        from_attributes = True  # ✅ Pydantic v2-compatible
