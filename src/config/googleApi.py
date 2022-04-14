from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
ls = "\n#############################################\n"


def googleApiConn():
    """
    Configure Google People API call
    """
    print("\n Connecting to Google People API ")
    # Setting parameters
    creds = None
    configPath = os.path.join(os.getcwd(), "src/config/")
    tokenJson = configPath + 'token.json'
    credentialsFile = configPath + 'credentials.json'

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/contacts']

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tokenJson):
        creds = Credentials.from_authorized_user_file(tokenJson, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsFile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenJson, 'w') as token:
            token.write(creds.to_json())

    # Creating Google Service
    service = build('people', 'v1', credentials=creds)

    try:
        print("\n Checking API Connection")
        # Call the People API
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=1,
            personFields='names').execute()
        connections = results.get('connections', [])

        if len(connections) >= 1:
            print("\n API connected successfully")
        else:
            print("\n Houston we have a problem")
            return False

    except HttpError as err:
        print("ERROR: HTTP Error")
        print(err)
        return False

    except Exception as err:
        print("ERROR: Credentials failed for some reason")
        print(err)
        return False

    return service


def getContacts(service):
    """
    Get list of 10 contacts to check which fields are we getting
    """
    try:
        print(ls, " Getting contacts from Google", ls)
        # Call the People API
        print('List 10 connection names')
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='names,emailAddresses').execute()
        connections = results.get('connections', [])

        for person in connections:
            print(person)
        """
        # Get specific field from list
        for person in connections:
            names = person.get('names', [])
            if names:
                name = names[0].get('displayName')
                print(name)
        """

    except Exception as err:
        print(" ERROR> Something failed while getting contacts list")
        print(err)


def createContact(service, contactInfo):
    """
    Create new contact
    Check fields in https://developers.google.com/people/api/rest/v1/people/createContact
    """
    try:
        print(ls, " Creating contact into Google", ls)

        name = contactInfo.get('name')
        familyName = contactInfo.get('familyName')
        telephone = contactInfo.get('telephone')
        emailAddress = contactInfo.get('emailAddress')

        response = service.people().createContact(body={
            "names": [
                {
                    "givenName": name,
                    "familyName": familyName
                }
            ],
            "phoneNumbers": [
                {
                    'value': telephone
                }
            ],
            "emailAddresses": [
                {
                    'value': emailAddress
                }
            ]
        }).execute()

        print(" Contact created successfully")
        print(response)

    except Exception as err:
        print(" ERROR> Something failed while creating contact")
        print(err)


def getContactUnique(service, contactInfo):
    """
    Get info about specific contact
    """
    try:
        print(ls, " Getting contact info from Google", ls)
        # Call the People API
        print('List contact info: ')
        name = contactInfo.get('name')
        familyName = contactInfo.get('familyName')
        print(name, ", ", familyName)

        results = service.people().searchContacts(
            pageSize=10,
            query=name,
            readMask='names').execute()

        if len(results) >= 1:
            print("\n Contact Found")
            print(results)

        else:
            print("\n Houston we have no contact in here")
            return False


    except Exception as err:
        print(" ERROR> Something failed while getting contacts list")
        print(err)
