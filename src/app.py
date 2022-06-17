import os
import pathlib
from dotenv import load_dotenv
from functools import lru_cache
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from .airtable import Airtable
from .update_class import UpdateAbout, UpdateExperience, UpdateUser

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
@app.get("/user/id/{user_id}")
def get_user_by_id(user_id:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_user_by_id(user_id)
    return res

@app.get("/user/name/{user_name}")
def get_user_by_user_name(user_name:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_user_by_user_name(user_name)
    return res



@app.patch("/user/{user_id}")
def update_user_by_id(user_id:str, update_user: UpdateUser):
    for attr in vars(update_user): #simple checking that requires firstname and lastname to always be there
        if vars(update_user)[attr] == None:
          return {"error in parsing request": "required first name and last name"}
    
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.update_user_by_id(user_id, update_user.first_name, update_user.last_name)
    return res

"""
ABOUT ENDPOINTS
"""
@app.get("/about/{user_name}")
def get_about_by_user_name(user_name:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_about_by_user_name(user_name)
    return res



@app.patch("/about/id/{about_id}")
def update_about_by_id(about_id: str, update_about:UpdateAbout):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.update_about_by_id(about_id, update_about.description)
    return res   

"""
EXPERIENCE ENDPOINTS
"""
@app.get("/experience/{user_name}")
def get_experience_by_user_name(user_name:str):
    airtable_client = Airtable(
        base_id=AIRTABLE_BASE_ID,
        api_key=AIRTABLE_API_KEY,
    )
    res = airtable_client.get_experience_by_user_name(user_name)
    return res

@app.patch("/experience/{experience_id}")
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