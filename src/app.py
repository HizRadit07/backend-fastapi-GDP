from os import abort
import pathlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from functools import lru_cache
from .controller.about_controller import router as about_router
from .controller.user_controller import router as user_router
from .controller.experience_controller import router as experience_router

BASE_DIR = pathlib.Path(__file__).parent # src

app = FastAPI()

@lru_cache()
def cache_dotenv():
    load_dotenv()

cache_dotenv()

origins =["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home_view():
    return{"hello":"there"}

app.include_router(about_router)
app.include_router(user_router)
app.include_router(experience_router)
