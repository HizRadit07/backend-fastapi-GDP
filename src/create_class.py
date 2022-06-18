from pydantic import BaseModel

class NewExperience(BaseModel):
    company_name: str
    company_logo_url: str
    job_title: str
    job_type: str
    date_start: str
    date_end: str
    location: str
    description: str