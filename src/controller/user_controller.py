from fastapi import Header, APIRouter
from ..service.airtable_service import Airtable
from ..models.user import UpdateUser
from ..service.firebase_service import *
from ..service.authentication_service import *
from ..loadenv import AIRTABLE_API_KEY, AIRTABLE_BASE_ID


"""
USER ENDPOINTS
"""
router = APIRouter()

@router.get("/user/id/{user_id}", tags=["User Endpoints"])
def get_user_by_id(user_id:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_user_by_id(user_id)
    return res

@router.get("/user/name/{user_name}", tags=["User Endpoints"])
def get_user_by_user_name(user_name:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_user_by_user_name(user_name)
    return res

@router.patch("/user/{user_id}", tags=["User Endpoints"])
def update_user_by_id(user_id:str, update_user: UpdateUser): 
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.update_user_by_id(user_id, update_user.first_name, update_user.last_name)
    return res

@router.get("/firebase/user/id/{user_id}", tags=["User Endpoints"])
def get_user_by_id_firebase(user_id:str):
    res = firebase_get_user_by_id(user_id)
    return res

@router.get("/firebase/user/name/{user_name}", tags=["User Endpoints"])
def get_user_by_name_firebase(user_name: str):
    res = firebase_get_user_by_name(user_name)
    return res

@router.patch("/firebase/user/{user_id}", tags=["User Endpoints"])
def update_user_by_id_firebase(user_id:str, update_user:UpdateUser, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_update_user_by_id(user_id, update_user)
    return res