from fastapi import Header, APIRouter
from ..service.airtable_service import Airtable
from ..models.about import UpdateAbout
from ..service.firebase_service import *
from ..service.authentication_service import *
from ..loadenv import AIRTABLE_API_KEY, AIRTABLE_BASE_ID

"""
ABOUT ENDPOINTS
"""
router = APIRouter()


@router.get("/about/{user_name}", tags=["About Endpoints"])
def get_about_by_user_name(user_name:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_about_by_user_name(user_name)
    return res



@router.patch("/about/{about_id}", tags=["About Endpoints"])
def update_about_by_id(about_id: str, update_about:UpdateAbout):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.update_about_by_id(about_id, update_about.description)
    return res   

@router.get("/firebase/about/{user_id}", tags=["About Endpoints"])
def get_about_by_user_id_firebase(user_id: str):
    res = firebase_get_about_by_user_id(user_id)
    return res

@router.patch("/firebase/about/{about_id}", tags=["About Endpoints"])
def update_about_by_id_firebase(about_id: str, update_about: UpdateAbout, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_update_about_by_id(about_id, update_about)
    return res
