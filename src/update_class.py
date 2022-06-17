from pydantic import BaseModel
from typing import Optional

class UpdateUser(BaseModel):
    first_name: str
    last_name: str

class UpdateAbout(BaseModel):
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