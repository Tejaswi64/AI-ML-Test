from manage_tables import db_connection
import os
from dotenv import load_dotenv
import psycopg2
import configparser
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sqlalchemy import create_engine
import pandas as pd

config = configparser.ConfigParser()
config.read('credentials.cfg')

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

    def create_branch_from_df():
       # Assuming you have a connection to the database
        try:
            # Database connection parameters
            DATABASE_TYPE = 'postgresql'
            DBAPI = 'psycopg2'
            ENDPOINT = config['postgres']['DB_HOST'] # e.g., localhost or remote server
            USER = config['postgres']['DB_USER']
            PASSWORD = config['postgres']['DB_PASSWORD']
            PORT = 5432 # Default PostgreSQL port
            DATABASE = config['postgres']['DB_NAME']
            # Creating the engine
            engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
            # Branches DataFrame
            df = pd.read_csv('branches.csv')
            # Saving DataFrame to PostgreSQL
            df.to_sql('branches', engine, if_exists='append', index=False)
            print("Data saved to PostgreSQL successfully.")
        except Exception as e:
            print("Error connecting to the database:", e)

    def create_branch_mongo_from_df():
        load_dotenv()
        uri = os.getenv("MONGO_DB_CONNECTION")
        client = MongoClient(uri, server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)
        db = client['members_test']
        collection = db['branches']
        try:
            # Branches DataFrame
            df = pd.read_csv('branches.csv')
            data_dict = df.to_dict(orient='records')
            collection.insert_many(data_dict)
            client.close()
            print("Data saved to mongodb successfully.")
        except Exception as e:
            print("Error connecting to the database:", e)

    def retrieve_branch_mongo_from_df(cls):
        load_dotenv()
        uri = os.getenv("MONGO_DB_CONNECTION")
        client = MongoClient(uri, server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)
        db = client['members_test']
        collection = db['branches']
        try:
            data = list(collection.find())
            df = pd.DataFrame(data)
            df['_id'] = df['_id'].astype(str)
            df.to_csv('branches_from_mongo.csv', index=False)
            client.close()
            print("Data read successfully.")
        except Exception as e:
            print("Error connecting to the database:", e)


#B = Branch(1, "BofA", "Park Ave", "Memphis", "38116")
#B = Branch(2, "Test", "test", "test", "test")
#print("**** Retrieve Branches ****")
#B.retrieve_branch()
#print("**** Creating a Branch ****")
#B.create_branch()
#print("**** Updating a Branch ****")
#B.update_branch(1,"BofA", "Jackson Street")
#B.delete_branch(2)
#B.create_branch_mongo_from_df()
#B.create_branch_mongo_from_df()
#B.retrieve_branch_mongo_from_df()