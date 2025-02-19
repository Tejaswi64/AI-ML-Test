from manage_tables import db_connection

class Branch:
    #class variable
    number_of_branches = 0

    def __init__(self, id, name, street, city, zip):
        #instance variable
        self.branch_id = id
        self.name = name
        self.street = street
        self.city = city
        self.zip = zip
        #connect here
        self.connection = db_connection()

    def retrieve_branch(self, branch_id=None):
        cursor = self.connection.cursor()
        if branch_id is None:
            query = "SELECT * FROM branch;"
        else:
            query = "SELECT * FROM branch where branch_id = %s ;"
        cursor.execute(query,(branch_id,))
        rows = cursor.fetchall()
        self.connection.commit()
        if rows:
            for row in rows:
                print(row)
            return rows
        else:
            print("No Branchs found")
    
    def create_branch(self ):
        if not self.retrieve_branch(self.branch_id):
            cursor = self.connection.cursor()
            cursor.execute(f"""
            INSERT INTO branch (branch_id, name, street, city, zip)
            VALUES (%s, %s, %s, %s, %s);
            """, (self.branch_id, self.name, self.street, self.city, self.zip))
            self.connection.commit()
            print("Branch inserted successfully!")
            #return cursor.fetchone()[0]
        else:
            print("Branch already exists")

    def update_branch(self, branch_id, name, street):
        if self.retrieve_branch(branch_id):
            cursor = self.connection.cursor()
            cursor.execute("""
            UPDATE branch
            SET name = %s,street = %s
                WHERE branch_id = %s;
            """, (name, street, branch_id))
            self.connection.commit()
            print("Branch updated successfully!")
            print("updated data")
            self.retrieve_branch()

    def delete_branch(self, branch_id):
        if self.retrieve_branch(branch_id):
            cursor = self.connection.cursor()
            cursor.execute(f"""
            DELETE FROM branch
            WHERE branch_id = %s;
            """, (branch_id,))
            self.connection.commit()
            print("Branch deleted successfully!")
        else:
            print("Branch not found")

#B = Branch(1, "BofA", "Park Ave", "Memphis", "38116")
B = Branch(2, "Test", "test", "test", "test")
print("**** Retrieve Branches ****")
B.retrieve_branch()
print("**** Creating a Branch ****")
B.create_branch()
#print("**** Updating a Branch ****")
#B.update_branch(1,"BofA", "Jackson Street")
#B.delete_branch(2)