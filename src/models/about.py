from pydantic import BaseModel

class UpdateAbout(BaseModel):
    description: str