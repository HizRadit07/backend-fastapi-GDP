from .firebase_service import firebase_app
from firebase_admin import auth


firebase_auth = auth.Client(firebase_app)

def backend_verify_id_token(token):
    try:
        decoded_token = firebase_auth.verify_id_token(token)
    except:
        return {"sucess":None,"error":"error in verifying token"}
    
    try:
        user_record = firebase_auth.get_user_by_email(decoded_token['email'])
        if(user_record.uid == decoded_token['user_id']):
            return {"success":"token verified","error":None}
        return{"sucess":None,"error":"token"}
    except:
        return {"sucess":None,"error":"user not found"}