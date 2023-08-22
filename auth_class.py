import requests
import base64
import json
import random
from dotenv import load_dotenv
import os
import sys

class ElationAPI_access:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.auth_token = base64.urlsafe_b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        self.auth_header = f"Basic {self.auth_token}"
        self.access_token = None
        self.physician_ids = []
        self.clinics_info = []

    def get_access_token(self):
        url = "https://sandbox.elationemr.com/api/2.0/oauth2/token/"
        response = requests.post(
            url,
            data={
                "username": self.username,
                "password": self.password,
                "grant_type": "password",
            },
            headers={'Authorization': self.auth_header}
        )
        response_data = response.json()
        self.access_token = response_data["access_token"]
        return self.access_token
    
    def format_auth(self):
        return f"Bearer {self.access_token}"
    
    def extract_info(self, response_data):
        data = json.loads(response_data)
        self.physician_ids = data["results"][0]["physicians"]
        self.clinics_info = [{"name": location["name"], "id": location["id"]} for location in data["results"][0]["service_locations"]]
    
    def fetch_and_extract_info(self):
        url = "https://sandbox.elationemr.com/api/2.0/practices/"
        resp = requests.get(url, headers={'Authorization': self.format_auth()})
        if resp.status_code == 200:
            self.extract_info(resp.content)
            return True
        else:
            print(f"Failed to fetch data. HTTP Status Code: {resp.status_code}")
            return False

    def list_clinics(self):
        for clinic in self.clinics_info:
            print(clinic["name"], "-", clinic["id"])
    
    def get_random_physician_id(self):
        return random.choice(self.physician_ids)

    def get_clinic_id_by_name(self, clinic_name):
        for clinic in self.clinics_info:
            if clinic["name"] == clinic_name:
                return clinic["id"]
        return None
    def get_clinic_practice_id_by_name(self, clinic_name):
        for clinic in self.clinics_info:
            if clinic["name"] == clinic_name:
                return 140976522133508
        return None

def display_help():
    help_text = """
    ElationAPI_access Help:

    To use the ElationAPI_access class, follow these steps:

    1. Initialize the class:
       api_access = ElationAPI_access()

    2. Obtain an access token:
       api_access.get_access_token()

    3. Fetch and extract clinic and physician information:
       api_access.fetch_and_extract_info()

    Available methods:
    - api_access.list_clinics(): Lists all available clinics with their names and IDs.
    - api_access.get_random_physician_id(): Returns a random physician ID.
    - api_access.get_clinic_id_by_name(clinic_name): Returns the ID for the given clinic name.

    """
    print(help_text)

if __name__ == "__main__":
    if "--help" in sys.argv:
        display_help()
    else:
        # Sample code to showcase usage
        api_access = ElationAPI_access()
        api_access.get_access_token()
        api_access.fetch_and_extract_info()
        api_access.list_clinics()
