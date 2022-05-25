import config.googleApi as people
import logging

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

    # Check Google API connection
    googleService = people.googleAPIConn()
    googleService.people().searchContacts(
        query='',
        readMask='names,emailAddresses').execute()

    # Contact Info (this comes from db)
    contactInfo = {
        'name': "José Rodriguez",
        'familyName': "12CABA",
        'telephone': "388470123",
        'emailAddress': 'mrodriguez@adkggm.com',
        'clientID': '002212'
    }

    # Check if contact exists. If it does, update all the matches,
    # otherwise it'll create it
    matches = people.getContactUnique(googleService, contactInfo)

    if matches is not None:
        print("Updating info of matching contacts")
        people.updateContact(googleService, matches, contactInfo)
    else:
        print("No contacts have been found, proceeding to create it")
        people.createContact(googleService, contactInfo)

    # Delete contact
    # people.deleteContact(googleService, matches)



if __name__ == '__main__':
    main()
