import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
from google.cloud.firestore import Client as FirestoreClient
from .create_class import NewExperience

load_dotenv()

cert = {
    "type": "service_account",
    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
    "private_key_id": "83f66b2d3c0bc913f18f35ba5ba0fe64ba78c0d0",
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "client_id": "106555114812167066499",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-hxjaz%40test-firebase-6fa94.iam.gserviceaccount.com"
  }


cred = credentials.Certificate(cert=cert)
firebase_admin.initialize_app(cred)

db: FirestoreClient = firestore.client()

"""
FIREBASE GET METHODS
"""
def firebase_get_user_by_id(id:str):
  user_doc_ref = db.collection("User").document(id)
  user_doc = user_doc_ref.get()
  #return a single document / instance by id
  if(not user_doc.exists):
    return {"error":"id not found"}
  return user_doc.to_dict()

def firebase_get_user_by_name(name:str):
  list_user = db.collection("User").where("Name","==",name).get()
  #return first user with that name
  if len(list_user) == 0:
    return {"error":"name not found"}
  return list_user[0].to_dict()

def firebase_get_about_by_user_id(user_id:str):
  list_about = db.collection("About").where("User","==",user_id).get()
  if len(list_about) == 0:
    return {"error":"about not found"}
  return list_about[0].to_dict()

def firebase_get_experience_by_user_id(user_id:str):
  list_experience = db.collection("Experience").where("User","==",user_id).get()
  if len(list_experience) == 0:
    return {"error":"experience not found"}
  return list_experience[0].to_dict()

"""
FIREBASE POST METHOD
"""
def firebase_create_new_experience_for_user(user_id:str, exp_data: NewExperience):
  data = {
    "Company Logo": exp_data.company_logo_url,
    "Company Name": exp_data.company_name,
    "Date End": exp_data.date_end,
    "Date Start": exp_data.date_start,
    "Description": exp_data.description,
    "Job Title": exp_data.job_title,
    "Job Type": exp_data.job_type,
    "Location": exp_data.location,
    "User": user_id
  }
  try:
    db.collection("Experience").add(data)
    return {"status":"sucess", "data":data}
  except:
    return {"error": "fail to add new data"}

