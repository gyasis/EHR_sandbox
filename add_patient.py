import requests
import json
from lxml import etree
from auth_class import ElationAPI_access
import sys

# Updating the parse_xml_and_match_fields function to include the corrected extraction logic for dob


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

    # Hardcoding the clinic name and then fetching its ID
    hardcoded_clinic_name = "Test Clinic 2"
    clinic_id = api_access.get_clinic_practice_id_by_name(hardcoded_clinic_name)
    
    if clinic_id is None:
        print(f"Clinic named {hardcoded_clinic_name} not found!")
        return None  # Return None if clinic not found

    patient_data["primary_physician"] = api_access.get_random_physician_id()
    patient_data["caregiver_practice"] = clinic_id

    resp = requests.post(
        "https://sandbox.elationemr.com/api/2.0/patients/",
        data=json.dumps(patient_data),
        headers={'Authorization': api_access.format_auth(),
                 'Content-type': 'application/json'}
    )

    print(resp.status_code)
    print(json.dumps(json.loads(resp.content), indent=2))

    # Return the patient's ID if the addition was successful
    if resp.status_code == 201:
        return resp.json().get('id')
    else:
        return None


def display_help():
    help_text = """
    main.py Help:

    - To process a single XML file and add a patient:
      python main.py /path/to/your/xml/file.xml

    - For help:
      python main.py --help

    """
    print(help_text)

if __name__ == "__main__":
    if "--help" in sys.argv:
        display_help()
    else:
        # Assuming the first argument is the path to the XML file
        xml_file_path = sys.argv[1]
        matched_data = parse_xml_and_match_fields(xml_file_path)
        patient_id = add_new_patient(matched_data)  # Storing the returned patient ID

        if patient_id:
            print(f"Patient added successfully with ID: {patient_id}")
        else:
            print("Failed to add patient.")
