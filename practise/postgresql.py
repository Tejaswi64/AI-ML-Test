import configparser
import os
from dotenv import load_dotenv
import psycopg2
from manage_tables import create_table
from members import create_member, retrieve_members, update_member, delete_member
from transactions import create_transaction, retrieve_transactions
from openai import OpenAI


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

retrieve_members(connection)


email = input("Please enter members email")
results = retrieve_members(connection, email)
print(results)
if(results is None):
    print("no member matched")
else:
    member_id=results[0][0]
    first_name = results[0][1]
    last_name = results[0][2]
#print(member_id, first_name, last_name)
transactions = retrieve_transactions(connection, str(member_id))
#print(transactions)
#print(transactions[0][3])
for i in transactions:
    print(i)

formatted_transactions = []
for trans in transactions:
    #print(trans)
    new_trans = {"amount":trans[3], "desc": trans[5], "datetrans": trans[2]}
    formatted_transactions.append(trans)

from chatgpt_api import summarize_assistant
summarize_assistant(first_name, last_name, formatted_transactions)




def responder(question):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a stock market analyzer"},
            {
                "role": "user",
                "content": question
            }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
question = input("Enter question")
responder(question)