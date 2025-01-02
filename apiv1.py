import requests
import json

# constants
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
API_BASE_URL = 'https://your-ministry-platform-domain.com'
TOKEN_URL = f'{API_BASE_URL}'/oauth2/token'
PROCEDURE_NAME = 'api_get_church_specific_events' # replace with procedure name

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

# Call the stored procedure
def call_procedure(access_token, procedure_name, params=None):
    url = f'{API_BASE_URL}/procs/{procedure_name}'
    headers = {
        'Authorization': F'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status() # Raise an error for bad responses
    return response.json()

# Parser
def parse_json_data(data):
    # check if the data is in a list
    if isinstance(data, list):
        for item in data:
            event_title = item.get('Event_Title')
            event_type_id = item.get('Event_Type_ID')
            minutes_for_setup = item.get('Minutes_for_Setup')
            event_start_date = item.get('Event_Start_Date')
            event_end_date = item.get('Event_End_Date')
            event_reservation_start = item.get('Event_Registration_Start')
            event_reservation_end = item.get('Event_Registration_End')
            minutes_for_cleanup = item.get('Minutes_For_Cleanup')
            cancelled = item.get('Cancelled')
            approved = item.get('_Approved')
            event_room_id = item.get('Event_Room_ID')
            room_id = item.get('Room_ID')
            print(f"Event_Title: {event_title}, Event_Type_ID: {event_type_id}, Minutes_For_Setup: {minutes_for_setup}, Event_Start_Date: {event_start_date}, Event_End_Date: {event_end_date}, Event_Reservation_Start: {event_reservation_start}, Event_Reservation_End: {event_reservation_end}, Minutes_For_Cleanup: {minutes_for_cleanup}, Cancelled: {cancelled}, Approved: {approved}, Event_Room_ID: {event_room_id}, Room_ID: {room_id}")
    else:
        print("The data is not in the expected list format.")

# Nested JSON
def parse_nested_json(data):
    group_name = data.get('GroupName')
    print(f"Group Name: {group_name}")
    
    members = data.get('Members', [])
    for member in members:
        id = member.get('ID')
        name = member.get('Name')
        email = member.get('Email')
        print(f"Member ID: {id}, Name: {name}, Email: {email}")

# Save JSON output
def save_json_to_file(data, filename='output.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

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
        print("Procedure call successful. Parsing data...")
        
        # Parse and Process
        parse_json_data(result)
        parse_nested_json(result)
        save_json_to_file(result)

    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")

# Run
if __name__ == '__main__':
    main()
