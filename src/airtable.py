from dataclasses import dataclass
import requests
from .util import *
from .update_class import UpdateExperience
from .create_class import NewExperience

@dataclass
class Airtable:
    base_id: str
    api_key: str

    """
    GET METHODS
    """
    def get_user_by_id(self, user_id:str):
        #method to create a synchronous request to get user by id to airtable
        endpoint = f"https://api.airtable.com/v0/{self.base_id}/User/{user_id}"
        headers={
            "Authorization": f"Bearer {self.api_key}"
        }
        try: #try with basic error handling fort any http error
            r = requests.get(endpoint, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        #return r.json when finish
        return r.json()
    
    def get_user_by_user_name(self, user_name:str):
        endpoint = f"https://api.airtable.com/v0/{self.base_id}/User?filterByFormula=%7BName%7D%3D'{user_name}'"
        headers={
            "Authorization": f"Bearer {self.api_key}"
        }
        try: #try with basic error handling fort any http error
            r = requests.get(endpoint, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        #return r.json when finish
        return r.json()

    def get_about_by_user_name(self, user_name:str):
        endpoint = f"https://api.airtable.com/v0/{self.base_id}/About?filterByFormula=%7BUser%7D%3D'{user_name}'"
        headers={
            "Authorization": f"Bearer {self.api_key}"
        }
        try: #try with basic error handling fort any http error
            r = requests.get(endpoint, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        #return r.json when finish
        return r.json()
    
    def get_experience_by_user_name(self, user_name:str):
        endpoint = f"https://api.airtable.com/v0/{self.base_id}/Experience?filterByFormula=%7BUser%7D%3D'{user_name}'"
        headers={
            "Authorization": f"Bearer {self.api_key}"
        }
        try: #try with basic error handling fort any http error
            r = requests.get(endpoint, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        #return r.json when finish
        return r.json()
    """
    UPDATE METHODS
    """
    def update_user_by_id(self, user_id: str, first_name: str, last_name: str):
        """TODO add more error handling for user input"""
        if (first_name == None or last_name == None):
            return {"error": "require first name & last name"}

        endpoint = f"https://api.airtable.com/v0/{self.base_id}/User"
        headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-type": "application/json"
        }
        patch_data = {
            "records":[
                {
                    "id": user_id,
                    "fields":{
                        "First Name": first_name,
                        "Last Name": last_name
                    }
                }
            ]
        }
        try: #try with basic error handling fort any http error
            r = requests.patch(endpoint, headers=headers, json=patch_data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return r.json()

    def update_about_by_id(self, about_id: str, description: str):
        """TODO add more error handling for user input"""

        endpoint = f"https://api.airtable.com/v0/{self.base_id}/About"
        headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-type": "application/json"
        }
        patch_data = {
            "records":[
                {
                    "id": about_id,
                    "fields":{
                        "Description": description
                    }
                }
            ]
        }
        try: #try with basic error handling fort any http error
            r = requests.patch(endpoint, headers=headers, json=patch_data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return r.json()

    def update_experience_by_id(self, experience_id:str, experience_data:UpdateExperience):
        """TODO add more error handling for user input"""

        endpoint = f"https://api.airtable.com/v0/{self.base_id}/Experience"
        headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-type": "application/json"
        }

        data_field = {
            "Company Name": experience_data.company_name,
            "Company Logo": [{
                "url": experience_data.company_logo_url
            }],
            "Job Title": experience_data.job_title,
            "Job Type": experience_data.job_type,
            "Date Start": experience_data.date_start, # date must be in format "YYYY-MM-DD or ISO 8061 format"
            "Date End": experience_data.date_end,
            "Location": experience_data.location,
            "Description": experience_data.description
        }

        if (experience_data.company_logo_url == None): #no new image url for update
            data_field.pop("Company Logo") #special case for company logo, adapt to data type
        
        data_field = remove_none_data(data_field) #remove any keys with None value
        
        patch_data = {
            "records":[
                {
                    "id": experience_id,
                    "fields":data_field
                }
            ]
        }
        try: #try with basic error handling fort any http error
            r = requests.patch(endpoint, headers=headers, json=patch_data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return r.json()
    """
    CREATE METHODS
    """   
    def create_new_experience_for_user(self, user_id: str, experience_data: NewExperience):
        """TODO add more error handling for user input"""
        """ add null checking for each field in data_field"""

        endpoint = f"https://api.airtable.com/v0/{self.base_id}/Experience"
        headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-type": "application/json"
        }

        data_field= {
            "User": [
                user_id
            ],
            "Company Name": experience_data.company_name,
            "Company Logo": [
                {
                    "url": experience_data.company_logo_url
                }
            ],
            "Job Title": experience_data.job_title,
            "Job Type": experience_data.job_type,
            "Date Start": experience_data.date_start,
            "Date End": experience_data.date_end,
            "Location": experience_data.location,
            "Description": experience_data.description
        }
        if (check_null_value_exist(data_field)):
            return {"error":"data field is missing some values"}

        post_data={
            "records": [
                { 
                    "fields":data_field
                }
            ]
        }

        try: #try with basic error handling fort any http error
            r = requests.post(endpoint, headers=headers, json=post_data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return r.json()

    """
    DELETE METHODS
    """
    def delete_experience_by_id(self, experience_id: str):
        endpoint = f"https://api.airtable.com/v0/{self.base_id}/Experience/{experience_id}"
        headers={
            "Authorization": f"Bearer {self.api_key}"
        }
        try: #try with basic error handling fort any http error
            r = requests.delete(endpoint, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return r.json()