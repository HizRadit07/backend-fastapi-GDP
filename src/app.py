import os
import pathlib
from dotenv import load_dotenv
from functools import lru_cache
from fastapi import FastAPI, Body, Header
from fastapi.middleware.cors import CORSMiddleware
from .airtable import Airtable
from .update_class import UpdateAbout, UpdateExperience, UpdateUser
from .create_class import NewExperience
from .firebase import *
from .authentication import backend_verify_id_token

BASE_DIR = pathlib.Path(__file__).parent # src

app = FastAPI()

origins =["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache()
def cache_dotenv():
    load_dotenv()

cache_dotenv()

AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")

@app.get("/")
def home_view():
    return{"hello":"there"}

"""
USER ENDPOINTS
"""
@app.get("/user/id/{user_id}", tags=["User Endpoints"])
def get_user_by_id(user_id:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_user_by_id(user_id)
    return res

@app.get("/user/name/{user_name}", tags=["User Endpoints"])
def get_user_by_user_name(user_name:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_user_by_user_name(user_name)
    return res

@app.patch("/user/{user_id}", tags=["User Endpoints"])
def update_user_by_id(user_id:str, update_user: UpdateUser): 
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.update_user_by_id(user_id, update_user.first_name, update_user.last_name)
    return res

@app.get("/firebase/user/id/{user_id}", tags=["User Endpoints"])
def get_user_by_id_firebase(user_id:str, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_get_user_by_id(user_id)
    return res

@app.get("/firebase/user/name/{user_name}", tags=["User Endpoints"])
def get_user_by_name_firebase(user_name: str, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_get_user_by_name(user_name)
    return res

@app.patch("/firebase/user/{user_id}", tags=["User Endpoints"])
def update_user_by_id_firebase(user_id:str, update_user:UpdateUser, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_update_user_by_id(user_id, update_user)
    return res

"""
ABOUT ENDPOINTS
"""
@app.get("/about/{user_name}", tags=["About Endpoints"])
def get_about_by_user_name(user_name:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_about_by_user_name(user_name)
    return res



@app.patch("/about/{about_id}", tags=["About Endpoints"])
def update_about_by_id(about_id: str, update_about:UpdateAbout):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.update_about_by_id(about_id, update_about.description)
    return res   

@app.get("/firebase/about/{user_id}", tags=["About Endpoints"])
def get_about_by_user_id_firebase(user_id: str, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_get_about_by_user_id(user_id)
    return res

@app.patch("/firebase/about/{about_id}", tags=["About Endpoints"])
def update_about_by_id_firebase(about_id: str, update_about: UpdateAbout, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_update_about_by_id(about_id, update_about)
    return res

"""
EXPERIENCE ENDPOINTS
"""
@app.get("/experience/{user_name}", tags=["Experience Endpoints"])
def get_experience_by_user_name(user_name:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_experience_by_user_name(user_name)
    return res

@app.patch("/experience/{experience_id}", tags=["Experience Endpoints"])
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

@app.post("/experience/{user_id}", tags=["Experience Endpoints"])
def create_new_experience_for_user(user_id: str, new_experience:NewExperience):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.create_new_experience_for_user(user_id, new_experience)    
    return res

@app.delete("/experience/{experience_id}", tags=["Experience Endpoints"])
def delete_experience_by_id(experience_id: str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.delete_experience_by_id(experience_id)   
    return res

@app.get("/firebase/experience/{user_id}", tags=["Experience Endpoints"])
def get_experience_by_user_id_firebase(user_id:str, id_token: str = Header(default=None)):
    # is_token_verified = backend_verify_id_token(id_token)
    # if (is_token_verified["error"] != None):
    #     return is_token_verified
    res = firebase_get_experience_by_user_id(user_id)
    return res

@app.post("/firebase/experience/{user_id}", tags=["Experience Endpoints"])
def create_experience_for_user_firebase(user_id: str, new_experience: NewExperience, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_create_new_experience_for_user(user_id, new_experience)
    return res

@app.patch("/firebase/experience/{experience_id}", tags=["Experience Endpoints"])
def update_experience_by_id_firebase(experience_id: str, update_experience: UpdateExperience, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_update_experience_by_id(experience_id, update_experience)
    return res

@app.delete("/firebase/experience/{experience_id}", tags=["Experience Endpoints"])
def delete_experience_by_id_firebase(experience_id:str, id_token: str = Header(default=None)):
    is_token_verified = backend_verify_id_token(id_token)
    if (is_token_verified["error"] != None):
        return is_token_verified
    res = firebase_delete_experience_by_id(experience_id)
    return res