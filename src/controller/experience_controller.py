from fastapi import Header, Body, APIRouter
from ..service.airtable_service import Airtable
from ..models.experience import NewExperience, UpdateExperience
from ..service.firebase_service import *
from ..service.authentication_service import *
from ..loadenv import AIRTABLE_API_KEY, AIRTABLE_BASE_ID



"""
EXPERIENCE ENDPOINTS
"""
router = APIRouter()

@router.get("/experience/{user_name}", tags=["Experience Endpoints"])
def get_experience_by_user_name(user_name:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_experience_by_user_name(user_name)
    return res

@router.patch("/experience/{experience_id}", tags=["Experience Endpoints"])
def update_experience_by_id(experience_id: str, update_experience: UpdateExperience = Body(
    default=None,
    example={
  "company_name": "GDP Labs",
  "job_title": "Software Engineering Intern",
  "job_type": "internship",
  "date_start": "2022-06-02",
  "date_end": "2022-08-05",
  "location": "Indonesia",
  "description": "I worked here",
  "company_logo_url": "https://picsum.photos/200"
}
)):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.update_experience_by_id(experience_id, update_experience)
    return res

@router.post("/experience/{user_id}", tags=["Experience Endpoints"])
def create_new_experience_for_user(user_id: str, new_experience:NewExperience):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.create_new_experience_for_user(user_id, new_experience)    
    return res

@router.delete("/experience/{experience_id}", tags=["Experience Endpoints"])
def delete_experience_by_id(experience_id: str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.delete_experience_by_id(experience_id)   
    return res

@router.get("/firebase/experience/{user_id}", tags=["Experience Endpoints"])
def get_experience_by_user_id_firebase(user_id:str):
    res = firebase_get_experience_by_user_id(user_id)
    return res

@router.post("/firebase/experience/{user_id}", tags=["Experience Endpoints"])
def create_experience_for_user_firebase(user_id: str, new_experience: NewExperience, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_create_new_experience_for_user(user_id, new_experience)
    return res

@router.patch("/firebase/experience/{experience_id}", tags=["Experience Endpoints"])
def update_experience_by_id_firebase(experience_id: str, update_experience: UpdateExperience, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_update_experience_by_id(experience_id, update_experience)
    return res

@router.delete("/firebase/experience/{experience_id}", tags=["Experience Endpoints"])
def delete_experience_by_id_firebase(experience_id:str, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_delete_experience_by_id(experience_id)
    return res