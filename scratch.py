# %%

from prettytable import PrettyTable

def display_clinic_table():
    # Fetch clinic data using the ElationAPI_access class
    api_access = ElationAPI_access()
    api_access.get_access_token()
    api_access.fetch_and_extract_info()

    # Create a table with headers
    table = PrettyTable()
    table.field_names = ["Clinic Name", "Clinic ID"]

    # Add rows to the table
    for clinic in api_access.clinics_info:
        table.add_row([clinic["name"], clinic["id"]])

    # Print the table
    print(table)

# Call the function to display the table
display_clinic_table()
