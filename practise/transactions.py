def create_transaction(connection, member_id, account, description, transaction_type = 'withdrawal'):
    cursor = connection.cursor()
    cursor.execute(f"""
    INSERT INTO fin_member_transactions ( member_id, account, description, transaction_type)
    VALUES (%s, %s, %s, %s) RETURNING transaction_id;
    """, (member_id, account, description, transaction_type))
    connection.commit()
    id = cursor.fetchone()[0]
    print("Record inserted successfully!")
    return id

def retrieve_transactions(connection, member_id=None):
    cursor = connection.cursor()
    if(member_id is None):
        query = "SELECT * FROM fin_member_transactions;"
    else:
        query = "SELECT * FROM fin_member_transactions where member_id = " + member_id
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.commit()
    #for row in rows:
    #    print(row)
    return rows