from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ls = "\n#############################################\n"


def googleAPIConn():
    """
    Configure Google People API call
    """
    print("\n Connecting to Google People API ")
    # Setting parameters
    creds = None
    configPath = os.path.join(os.getcwd(), "./config/")
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
        connections = getContacts(service, 1)

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


def getContacts(service, qty, show=False):
    """
    Get list of contacts to check which fields are we getting
    """
    try:
        print(" Trying to read contacts from Google")
        # Call the People API
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=qty,
            personFields='names,emailAddresses,phoneNumbers').execute()
        connections = results.get('connections', [])

        if show:
            print(f'List {qty} connection names')
            for person in connections:
                print(person)

        return connections

    except Exception as err:
        print(" ERROR> Something failed while getting contacts list")
        print(err)


def createBody(contactInfo):
    """
    Creates structure for API post
    """
    name = contactInfo.get('name')
    familyName = contactInfo.get('familyName')
    telephone = contactInfo.get('telephone')
    emailAddress = contactInfo.get('emailAddress')
    clientID = contactInfo.get('clientID')

    body = {
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
        ],
        "nicknames": [
            {
                'value': clientID
            }
        ]
    }

    return body


def createContact(service, contactInfo):
    """ 
    Create new contact
    Check fields in https://developers.google.com/people/api/rest/v1/people/createContact
    """
    try:
        print(ls, " Creating contact into Google", ls)

        body = createBody(contactInfo)

        response = service.people().createContact(body=body).execute()

        print(" Contact created successfully")
        print(response)

    except Exception as err:
        print(" ERROR> Something failed while creating contact")
        print(err)


def getContactUnique(service, contactInfo):
    """
    Get info about specific contact
    Returns the matched qty and the contacts
    """
    try:
        print(ls, " Getting contact info from Google", ls)
        name = contactInfo.get('name')
        familyName = contactInfo.get('familyName')
        clientID = contactInfo.get('clientID')

        print(f' Searching in contacts list for: {clientID}, {name}, {familyName}')

        results = service.people().searchContacts(
            pageSize=10,
            query=clientID,
            readMask='names').execute()

        results = results.get("results")

        if results is not None:
            print(f"\n Matches found: {len(results)}")
            print(results)
            return results

        else:
            print("\n Matches found: 0")
            return None

    except Exception as err:
        print(" ERROR> Something failed while getting contacts list")
        print(err)


def updateContact(service, contactsUpdate, contactInfo):
    """
    Update old contact
    Check fields in https://developers.google.com/people/api/rest/v1/people/updateContact
    """
    try:
        print(ls, " Updating contact into Google", ls)

        for contact in contactsUpdate:
            print(contact)
            contact = contact.get('person')
            names = contact.get('names')[0]

            name = names.get('displayName')
            familyName = names.get('familyName')

            resourceID, etag = getContactTag(contact)

            print(f"{name}, {familyName}, {resourceID}, {etag}")

            response = service.people().updateContact(
                updatePersonFields='names,phoneNumbers,emailAddresses',
                resourceName=resourceID,
                body={
                    "etag": etag,
                    "names": [
                        {
                            "givenName": contactInfo.get('name'),
                            "familyName": contactInfo.get('familyName')
                        }
                    ],
                    "phoneNumbers": [
                        {
                            'value': contactInfo.get('telephone')
                        }
                    ],
                    "emailAddresses": [
                        {
                            'value': contactInfo.get('emailAddress')
                        }
                    ]
                }).execute()

            print(" Contact updated successfully")
            print(response)

    except Exception as err:
        print(" ERROR> Something failed while creating contact")
        print(err)


def deleteContact(service, contactsDelete):
    """
    Delete old contact
    Check fields in https://developers.google.com/people/api/rest/v1/people/deleteContact
    """
    try:
        print(ls, " Deleting contact from Google", ls)

        for contact in contactsDelete:
            contact = contact.get('person')

            resourceID, etag = getContactTag(contact)
            print(f"well hello there {resourceID}, and {etag}")
            response = service.people().deleteContact(
                resourceName=resourceID
                ).execute()

            print(" Contact deleted successfully")
            print(response)

    except Exception as err:
        print(" ERROR> Something failed while deleting contact")
        print(err)


def getContactTag(contact):
    resourceID = contact.get('resourceName')
    etag = contact.get('etag')

    return resourceID, etag


def updateGooglebyDatabase():
    """
    TODO under development
    JUST USE THIS IN CASE GOOGLE CONTACTS ISN'T UPDATED
    """

    # find matches by number, name or email
    # update with client id

