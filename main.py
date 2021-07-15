# This is one of the excellent python projects for beginners. Everyone uses a contact book to save contact details,
# including name, address, phone number, and even email address. This is a command-line project where you will design
# a contact book application that users can use to save and find contact details. The application should also allow
# users to update contact information, delete contacts, and list saved contacts. The SQLite database is the ideal
# platform for saving contacts. To handle a project with Python for beginners can be helpful to build your career
# with a good start.
from configparser import ConfigParser
import psycopg2


def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} not found in the {1} file.".format(section,filename))

    return db


def add_contact(name, address, phone, email):

    params = config()
    conn = None

    try:
        # Connect to server
        print("Connecting to Database...")
        conn = psycopg2.connect(**params)

        cursor = conn.cursor()

        # Add customer
        cursor.execute("insert into \"Contacts\" (\"ContactName\", \"Address\", \"Phone\", \"Email\") values ("
                       "%s, %s, %s, "
                       "%s)", (name, address, int(phone), email))

        cursor.close()

        print("Contact successfully added.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


def update_contact(id, name, address, phone, email):

    params = config()
    conn = None

    try:
        # Connect to server
        print("Connecting to Database...")
        conn = psycopg2.connect(**params)

        cursor = conn.cursor()
        cursor.prepare("update Contacts set name=%s, address=%s, phone=%s, email=%s where id=%s")
        cursor.execute(name, address, phone, email, id)
        cursor.close()

        print("Contacts successfully retrieved.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


def delete_contact(id):

    params = config()
    conn = None

    try:
        # Connect to server
        print("Connecting to Database...")
        conn = psycopg2.connect(**params)

        cursor = conn.cursor()
        cursor.prepare("delete from Contacts where id = %s")
        cursor.execute(id)
        cursor.close()

        print("Contact successfully deleted.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


def list_contacts():
    params = config()
    conn = None

    try:
        # Connect to server
        print("Connecting to Database...")
        conn = psycopg2.connect(**params)

        cursor = conn.cursor()
        cursor.execute("select * from Contacts")
        cursor.close()

        print("Contacts successfully retrieved.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


if __name__ == '__main__':
    print("Welcome back to your ContactBook!")
    user_input = input("What do you want to do?\n"
          "'a' - Add a new contact\n"
          "'u' - Update a contact\n"
          "'d' - Delete a contact\n"
          "'l' - List all contacts\n"
          "'x' - Exit Application\n")

    while user_input != "x":
        if user_input == "a":
            name = input("Enter Name: ")
            address = input("Enter Address: ")
            phone = input("Enter Phone: ")
            email = input("Enter Email: ")
            add_contact(name, address, phone, email)
        if user_input == "u":
            index = input("Enter Contact Index which should be updated:\n")
            name = input("Enter Name:\n")
            address = input("Enter Address:\n")
            phone = input("Enter Phone:\n")
            email = input("Enter Email:\n")
            update_contact(index, name, address, phone, email)
        if user_input == "d":
            index = input("Enter Contact Index which should be deleted:\n")
            delete_contact(index)
        if user_input == "l":
            print("List of all Contacts:\n")
            list_contacts()
    exit()