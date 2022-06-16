import os
import pathlib
from dotenv import load_dotenv
from functools import lru_cache
from fastapi import FastAPI
from .airtable import Airtable

BASE_DIR = pathlib.Path(__file__).parent # src

app = FastAPI()

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