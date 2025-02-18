class Member:

    member_serial_number = 0

    def __init__(self, email, fname=None, lname=None,  age=None, address=None, salary=None):
        self.id = None
        self.first_name = fname
        self.last_name = lname
        self.email = email
        self.phone_number = None
        self.date_of_birth = None
        self.age = age
        self.address = address
        self.salary = salary
        self.__ssn = None
        self.db_connection()
    
    def db_connection(self):
        import os
        from dotenv import load_dotenv
        import psycopg2

        # Load environment variables from .env file
        load_dotenv()

        # Database connection setup
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                sslmode="require"
            )
            print("Database connection successful!")
        except Exception as e:
            print("Error connecting to the database",e)

    def retrieve_member(self, email=None):
        cursor = self.connection.cursor()
        if email is None:
            query = "SELECT * FROM fin_members;"
        else:
            query = "SELECT * FROM fin_members where email = %s ;"
        cursor.execute(query,(email,))
        rows = cursor.fetchall()
        self.connection.commit()
        if rows:
            for row in rows:
                print(row)
            return rows
        else:
            print("No records found")
    
    def create_new_member(self ):
        if not self.retrieve_member(self.email):
            cursor = self.connection.cursor()
            cursor.execute(f"""
            INSERT INTO fin_members (first_name, last_name, email, phone_number, date_of_birth)
            VALUES (%s, %s, %s, %s, %s);
            """, (self.first_name, self.last_name, self.email, self.phone_number, self.date_of_birth))
            self.connection.commit()
            #id = cursor.fetchone()[0]
            print("Record inserted successfully!")
        else:
            print("Member already exists")

    def update_member(self, email, first_name, last_name):
        if self.retrieve_member(email):
            cursor = self.connection.cursor()
            cursor.execute("""
            UPDATE fin_members
            SET first_name = %s, last_name = %s
                WHERE email = %s;
            """, (first_name, last_name, email))
            self.connection.commit()
            print("Record updated successfully!")
            print("updated data")
            self.retrieve_member()

    def delete_member(self, email):
        r = self.retrieve_member(email)
        if r:
            cursor = self.connection.cursor()
            cursor.execute(f"""
            DELETE FROM fin_members
            WHERE email = %s;
            """, (email,))
            self.connection.commit()
            print("Record deleted successfully!")
        else:
            print("Record not found")

M = Member('test1@fin.com','Test1','Test1')
print("****** Creating a new member ******")
M.create_new_member()
print("****** Checking member ******")
print(M.retrieve_member('tk@fin.com'))
print("****** Retriving all members ******")
M.retrieve_member()
print("****** Deleting ******")
M.delete_member('test1@fin.com')
print("****** Retriving all members ******")
M.retrieve_member()
print("****** Updating Record ******")
M.update_member('test@fin.com', 'test_updated', 'test_updated')



