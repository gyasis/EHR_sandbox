import requests
import json
from lxml import etree
from auth_class import ElationAPI_access
import sys
import base64
import os

def parse_xml_and_match_fields(file_path):
    # Parsing using lxml
    tree = etree.parse(file_path)
    root = tree.getroot()

    # Namespace mapping
    nsmap = {'ns': 'urn:hl7-org:v3'}

    # Extracting patient-related information
    matched_data = {
        "first_name": None,
        "last_name": None,
        "sex": None,
        "dob": None
    }

    # Extracting name
    first_name_element = root.xpath(".//ns:given", namespaces=nsmap)
    last_name_element = root.xpath(".//ns:family", namespaces=nsmap)
    if first_name_element:
        matched_data["first_name"] = first_name_element[0].text
    if last_name_element:
        matched_data["last_name"] = last_name_element[0].text

    # Extracting sex
    gender_code_element = root.xpath(".//ns:administrativeGenderCode", namespaces=nsmap)
    if gender_code_element:
        gender_code = gender_code_element[0].get("code")
        if gender_code == "F":
            matched_data["sex"] = "Female"
        elif gender_code == "M":
            matched_data["sex"] = "Male"

    # Extracting date of birth
    dob_element = root.xpath(".//ns:birthTime", namespaces=nsmap)
    if dob_element:
        dob_value = dob_element[0].get("value")
        matched_data["dob"] = f"{dob_value[:4]}-{dob_value[4:6]}-{dob_value[6:8]}"

    return matched_data



def add_new_patient(patient_data):
    api_access = ElationAPI_access()
    api_access.get_access_token()
    api_access.fetch_and_extract_info()

    hardcoded_clinic_name = "Test Clinic 2"
    clinic_id = api_access.get_clinic_practice_id_by_name(hardcoded_clinic_name)
    
    if clinic_id is None:
        print(f"Clinic named {hardcoded_clinic_name} not found!")
        return None

    patient_data["primary_physician"] = api_access.get_random_physician_id()
    patient_data["caregiver_practice"] = clinic_id

    resp = requests.post(
        "https://sandbox.elationemr.com/api/2.0/patients/",
        data=json.dumps(patient_data),
        headers={'Authorization': api_access.format_auth(),
                 'Content-type': 'application/json'}
    )

    if resp.status_code == 201:
        patient_id = resp.json().get('id')
        return patient_id
    else:
        print(resp.status_code)
        print(json.dumps(json.loads(resp.content), indent=2))
        return None

def submit_clinical_document(patient_id, xml_file_path, clinic_name):
    # Convert XML to Base64
    with open(xml_file_path, 'rb') as file:
        base64_content = base64.b64encode(file.read()).decode('utf-8')
    
    api_access = ElationAPI_access()
    api_access.get_access_token()
    api_access.fetch_and_extract_info()
    
    # Fetching the clinic practice ID dynamically
    authoring_practice_id = api_access.get_clinic_practice_id_by_name(clinic_name)
    if not authoring_practice_id:
        print(f"Couldn't find the clinic named {clinic_name}.")
        return

    data = {
      "patient": patient_id,
      "authoring_practice": authoring_practice_id,
      "xml_file": {
        "original_filename": os.path.basename(xml_file_path),  # Using just the file's name
        "content_type": "application/octet-stream",
        "base64_content": base64_content
      },
      "data_format": "ccda"
    }

    resp = requests.post(
        "https://sandbox.elationemr.com/api/2.0/clinical_documents/",
        data=json.dumps(data),
        headers={'Authorization': api_access.format_auth(),
                 'Content-type': 'application/json'}
    )

    print(resp.status_code)
    print(json.dumps(json.loads(resp.content), indent=2))

# [Include the display_help function here]

if __name__ == "__main__":
    if "--help" in sys.argv:
        display_help()
    else:
        # Assuming the first argument is the path to the XML file
        xml_file_path = sys.argv[1]
        matched_data = parse_xml_and_match_fields(xml_file_path)
        patient_id = add_new_patient(matched_data)
        # If a patient was successfully added, submit the clinical document
        if patient_id:
            hardcoded_clinic_name = "Test Clinic 2"  # Replace with your desired clinic name
            submit_clinical_document(patient_id, xml_file_path, hardcoded_clinic_name)