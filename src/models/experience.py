from pydantic import BaseModel
from typing import Optional

class NewExperience(BaseModel):
    company_name: str
    company_logo_url: str
    job_title: str
    job_type: str
    date_start: str
    date_end: str
    location: str
    description: str

class UpdateExperience(BaseModel):
    company_name: Optional[str]= None
    job_title: Optional[str]= None
    job_type: Optional[str]= None
    date_start: Optional[str]= None
    date_end: Optional[str]= None
    location: Optional[str]= None
    description: Optional[str]= None
    company_logo_url: Optional[str]= None