import requests

# constants
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
API_BASE_URL = 'https://your-ministry-platform-domain.com'
TOKEN_URL = f'{API_BASE_URL}'/oauth2/token'
PROCEDURE_NAME = 'YourProcedureName' # replace with procedure name

# Authentication
def get_access_token():
    auth_data = {
        'grant-type': 'client-credentials',
        'client-id': CLIENT_ID,
        'client-secret': CLIENT_SECRET,
        'scope': 'http://thinkministry.com/dataplatform/scopes/all'
    }
    response = requests.post(TOKEN_URL, data=auth_data)
    response.raise_for_status() # Raise an error for bad responses
    return response.json()['access_token']

# Call stored procedure
def main():
    try:
        # Get access token
        access_token = get_access_token()
        print("Access token retrieved successfully.")

        # Call the procedure
        procedure_params = {
            'Param1': 'Value1', # replace with actual parameters if needed
            'Param2': 'Value2'
        }
        result = call_procedure(access_token, PROCEDURE_NAME, params=procedure_params)
        print("Procedure call successful. Result:")
        print(result)

    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")

# Run
if __name__ == '__main__':
    main()
