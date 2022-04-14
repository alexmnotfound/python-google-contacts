import config.googleApi as people


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

    #
    # Check Google API connection
    #
    googleService = people.googleApiConn()

    # Check Contacts
    # people.getContacts(googleService)

    # Contact Info
    contactInfo = {
        'name': "Matias Rodriguez",
        'familyName': "12CABA",
        'telephone': "3884701269",
        'emailAddress': 'mrodriguez@ggggm.com'
    }


    # Create Contact
    people.createContact(googleService, contactInfo)

    # Get Single contact info
    people.getContactUnique(googleService, contactInfo)


if __name__ == '__main__':
    main()
