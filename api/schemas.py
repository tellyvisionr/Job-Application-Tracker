from pydantic import BaseModel
from datetime import date
from typing import Optional


class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: str = "Applied"
    date_applied: date
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    date_applied: Optional[date] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    notes: Optional[str] = None


class ApplicationResponse(ApplicationCreate):
    id: int

    class Config:
        from_attributes = True
