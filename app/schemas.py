from pydantic import BaseModel, EmailStr, Field

class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str

class CompanyOut(CompanyCreate):
    id: int
    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    company_id: int
    title: str = Field(min_length=2, max_length=150)
    description: str
    skills: list[str] = []

class JobOut(JobCreate):
    id: int
    class Config:
        from_attributes = True

class CandidateCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str
    skills: list[str] = []

class CandidateOut(CandidateCreate):
    id: int
    class Config:
        from_attributes = True
