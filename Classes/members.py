

class Member:

    member_serial_number = 0

    def __init__(self, email=None, fname=None, lname=None,  phone_number = None, dob = None, age=None, address=None, salary=None,):
        self.id = None
        self.first_name = fname
        self.last_name = lname
        self.email = email
        self.phone_number = None
        self.age = age
        self.address = address
        self.salary = salary
        self.date_of_birth = dob
        self.__ssn = None

    @staticmethod
    def retrieve_serial_number_static():
        return Member.member_serial_number
    
    @classmethod
    def retrieve_serial_number_class(cls):
        #return cls.member_serial_number both are valid
        return Member.member_serial_number
    
    #private method
    def __retrieve_ssn(self):
        print(self.__ssn)

    def retrieve_member_details(self):
        member_serial_number = 20
        #Retrieve details from database using Email
        return "details"
    
    def create_new_member(self):
        import configparser
        import os
        from dotenv import load_dotenv
        import psycopg2
        from manage_tables import create_table
        #from members import create_member, retrieve_members, update_member, delete_member
        #from transactions import create_transaction, retrieve_transactions


        # Initialize the config parser
        config = configparser.ConfigParser()
        config.read('credentials.cfg')

        # Database connection details
        # Default PostgreSQL port
        # Establishing the connection
        try:
            connection = psycopg2.connect(
                dbname=config['postgres']['DB_NAME'],
                user=config['postgres']['DB_USER'],
                password=config['postgres']['DB_PASSWORD'],
                host=config['postgres']['DB_HOST'],
                port=config['postgres']['DB_PORT'],
                sslmode="require"
            )
            print("Database connection successful!")
        except Exception as e:
            print("Error connecting to the database:", e)

        #2.3 Creating a Cursor Object and Executing Queries
        #Once connected, a cursor object is used to execute SQL queries:

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        print("PostgreSQL version:", cursor.fetchone())

        #2.4 Closing the Connection
        #After performing database operations, always close the connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")


        try:
            connection = psycopg2.connect(
                dbname=config['postgres']['DB_NAME'],
                user=config['postgres']['DB_USER'],
                password=config['postgres']['DB_PASSWORD'],
                host=config['postgres']['DB_HOST'],
                port=config['postgres']['DB_PORT'],
                sslmode="require"
            )
            print("Database connection successful!")
        except Exception as e:
            print("Error connecting to the database:", e)
        create_table(connection, "members")
        create_table(connection, "transactions")
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO fin_members (first_name, last_name, email, phone_number, date_of_birth)
        VALUES (%s, %s, %s, %s, %s);
        """, (self.first_name, self.last_name, self.email, self.phone_number, self.date_of_birth))
        connection.commit()
        #id = cursor.fetchone()[0]
        print("Record inserted successfully!")
        #return id
    

new_member = Member('test@fin.com', 'Test', 'Test')

print(new_member.member_serial_number)
print(Member.member_serial_number)

print(new_member.first_name)

print(new_member.create_new_member())
