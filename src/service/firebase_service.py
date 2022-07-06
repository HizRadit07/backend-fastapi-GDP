import imp
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
from google.cloud.firestore import Client as FirestoreClient
from ..models.experience import NewExperience, UpdateExperience
from ..models.about import UpdateAbout
from ..models.user import UpdateUser
from ..util import *

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
firebase_app = firebase_admin.initialize_app(cred)

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
  arr_experience = []
  for item in list_experience:
    arr_experience.append(item.to_dict())

  return arr_experience 

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

"""
FIREBASE UPDATE METHOD
"""
def firebase_update_user_by_id(user_id:str, update_user:UpdateUser):
  if (update_user.first_name == None or update_user.last_name == None):
      return {"error": "require first name & last name"}

  data = {
    "First Name": update_user.first_name,
    "Last Name": update_user.last_name,
    "Name": str(update_user.first_name+" "+update_user.last_name)
  }

  try:
    db.collection("User").document(user_id).update(data)
    return {"status":"sucess", "data":data}
  except:
    return {"error": "fail to add new data"} 
 
def firebase_update_about_by_id(about_id:str, update_about:UpdateAbout):
  if (update_about.description == None):
    return {"error": "require description"}
  data = {
    "Description": update_about.description
  }
  try:
    db.collection("About").document(about_id).update(data)
    return {"status":"sucess", "data":data}
  except:
    return {"error": "fail to add new data"}

def firebase_update_experience_by_id(experience_id: str, update_experience: UpdateExperience):
  data = {
    "Company Logo": update_experience.company_logo_url,
    "Company Name": update_experience.company_name,
    "Date End": update_experience.date_end,
    "Date Start": update_experience.date_start,
    "Description": update_experience.description,
    "Job Title": update_experience.job_title,
    "Job Type": update_experience.job_type,
    "Location": update_experience.location,
  }
  data = remove_none_data(data) #remove key with none value to not update
  try:
    db.collection("Experience").document(experience_id).update(data)
    return {"status":"sucess", "data":data}
  except:
    return {"error": "fail to add new data"}

"""
FIREBASE DELETE METHODS
"""
def firebase_delete_experience_by_id(experience_id: str):
  try:
    db.collection("Experience").document(experience_id).delete()
    return {"status":"sucess"}
  except:
    return {"error": "fail to add new data"}