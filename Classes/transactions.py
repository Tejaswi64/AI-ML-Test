from members import Member

class Transactions:

    def __init__(self, first_name, last_name, email, account, description, transaction_type = 'withdrawal'):
        self.id = None
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.account = account
        self.description = description
        self.transaction_type = 'withdrawal'
        self.member = Member(email, first_name, last_name)
        self.connection = self.member.connection

    def retrieve_transaction(self, email=None):
        cursor = self.connection.cursor()
        if(email is None):
            query = "SELECT * FROM fin_member_transactions;"
        else:
            query = "SELECT * FROM fin_member_transactions where member_id = " + str(self.retrieve_member_id(email))
        cursor.execute(query, (self.retrieve_member_id(email),))
        rows = cursor.fetchall()
        self.connection.commit()
        for row in rows:
            print(row)
        return rows
    
    def create_transaction(self,email=None):
        cursor = self.connection.cursor()
        cursor.execute(f"""
        INSERT INTO fin_member_transactions ( member_id, account, description, transaction_type)
        VALUES (%s, %s, %s, %s) RETURNING transaction_id;
        """, (self.retrieve_member_id(self.email), self.account, self.description, self.transaction_type))
        self.connection.commit()
        id = cursor.fetchone()[0]
        print("Record inserted successfully!")
        return id
    
    def retrieve_member_id(self, email):
        #M = Member(email, self.first_name, self.last_name)
        results = self.member.retrieve_member(email)
        if not results:
            self.member.create_member()
            results = self.member.retrieve_member(email)
        return results[0][0]

    '''def update_transaction(self, email, first_name, last_name):
        if self.retrieve_member(email):
            cursor = self.connection.cursor()
            cursor.execute("""
            UPDATE fin_members_transactions
            SET first_name = %s, last_name = %s
                WHERE email = %s;
            """, (first_name, last_name, email))
            self.connection.commit()
            print("Record updated successfully!")
            print("updated data")
            self.retrieve_member()'''

    '''def delete_transaction(self, email):
        r = self.retrieve_member(email)
        if r:
            cursor = self.connection.cursor()
            cursor.execute(f"""
            DELETE FROM fin_members_transactions
            WHERE email = %s;
            """, (email,))
            self.connection.commit()
            print("Record deleted successfully!")
        else:
            print("Record not found")'''

T = Transactions('Test3', 'Test3','test3@fin.com','30','food')

print("***** All Transactions *****")
T.retrieve_transaction('test1@fin.com')

T.create_transaction()