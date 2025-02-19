from manage_tables import db_connection
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
        self.connection = db_connection()

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
            print("No Members found")
    
    def create_member(self ):
        if not self.retrieve_member(self.email):
            cursor = self.connection.cursor()
            cursor.execute(f"""
            INSERT INTO fin_members (first_name, last_name, email, phone_number, date_of_birth)
            VALUES (%s, %s, %s, %s, %s) RETURNING member_id;
            """, (self.first_name, self.last_name, self.email, self.phone_number, self.date_of_birth))
            self.connection.commit()
            print("Member inserted successfully!")
            #return cursor.fetchone()[0]
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
            print("Member updated successfully!")
            print("updated data")
            self.retrieve_member()

    def delete_member(self, email):
        if self.retrieve_member(email):
            cursor = self.connection.cursor()
            cursor.execute(f"""
            DELETE FROM fin_members
            WHERE email = %s;
            """, (email,))
            self.connection.commit()
            print("Member deleted successfully!")
        else:
            print("Member not found")

'''
M = Member('test1@fin.com','Test1','Test1')
print("****** Creating a new member ******")
M.create_member()
print("****** Checking member ******")
print(M.retrieve_member('tk@fin.com'))
print("****** Retriving all members ******")
M.retrieve_member()
print("****** Deleting ******")
M.delete_member('test1@fin.com')
print("****** Retriving all members ******")
M.retrieve_member()
print("****** Updating Member ******")
M.update_member('test@fin.com', 'test_updated', 'test_updated')

M = Member('test1@fin.com','Test1','Test1')
M.delete_member('test2@fin.com')
'''