---
noteId: "e1f9d75040cb11ee9a09a140fa7e3f5e"
tags: []

---

# EHR_sandbox 

## Overview

## Requirement

## Usage

# ElationAPI_access

This is a Python class that provides access to the Elation API using OAuth2 authentication.

## Usage

To use this class, you will need to create a `.env` file in the same directory as your `Authenticate.py` file with the following contents:

```

CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
USERNAME=your_username
PASSWORD=your_password
```

Replace `your_client_id` , `your_client_secret` , `your_username` , and `your_password` with your actual credentials.

Then, in your `Authenticate.py` file, import the `dotenv` package and load the environment variables from the `.env` file:

```python
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
```

Finally, create an instance of the `ElationAPI_access` class and use the `get_access_token` and `format_auth` methods to authenticate and make API requests:

```python
from ElationAPI_access import ElationAPI_access

api_access = ElationAPI_access()

access_token = api_access.get_access_token()

auth_header = api_access.format_auth()

response = requests.get(
    "https://sandbox.elationemr.com/api/2.0/practices/",
    headers={'Authorization': auth_header}
)

print(response.status_code)
print(json.dumps(json.loads(response.content), indent=2))
```

Make sure to replace `https://sandbox.elationemr.com/api/2.0/practices/` with the actual API endpoint you want to access.

## Features

## Reference

## Author

## License

Please see license.txt.
