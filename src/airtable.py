from dataclasses import dataclass
import requests

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

    

