from pydantic import BaseModel

class UpdateUser(BaseModel):
    first_name: str
    last_name: str