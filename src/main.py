import config.googleApi as people
import sys


def main():
    """
        Google People API for contacts management

    1. Check connection to Google API
    2. Check connection to SQL
    3. New Contacts:
        - Get contacts to create from SQL
        - Create new contacts in Google
        - Update created contacts in SQL
    4. Update Contacts:
        - Get contacts to update from SQL
        - Get contacts to update from Google
        - Update contacts in Google
        - Update created contacts in SQL

    """
    ls = "\n#############################################\n"
    print(ls, 'Google People API for contacts management.', ls)

    # get mode as delete or create
    mode = str(sys.argv[1])

    allowedModes = ["delete", "create"]

    if mode in allowedModes:
        runProcess(mode)
    else:
        print(f"ERROR: argument {mode} is not allowed, try with {allowedModes}")


def runProcess(mode):
    print(f"Starting script for {mode} contact")
    # Check Google API connection
    googleService = people.googleAPIConn()
    googleService.people().searchContacts(
        query='',
        readMask='names,emailAddresses').execute()

    # Contact Info (this comes from db)
    contactInfo = {
        'name': "Matias Alejandro Rodriguez",
        'familyName': "12CABA",
        'telephone': "3884701234",
        'emailAddress': 'mrodriguez@jotmeil.com',
        'clientID': '002212'
    }

    # Check if contact exists. If it does, update all the matches,
    # otherwise it'll create it
    matches = people.getContactUnique(googleService, contactInfo)

    if mode == "create":
        if matches is not None:
            print("Updating info of matching contacts")
            people.updateContact(googleService, matches, contactInfo)
        else:
            print("No contacts have been found, proceeding to create it")
            people.createContact(googleService, contactInfo)

    if mode == "delete":
        # Delete contact
        if matches is not None:
            people.deleteContact(googleService, matches)


if __name__ == '__main__':
    main()
