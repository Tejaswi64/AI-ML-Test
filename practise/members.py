def greet(name):
    return f"Hello, {name}!"



def create_member(connection, first_name, last_name, email, phone_number=None, date_of_birth=None):
    cursor = connection.cursor()
    cursor.execute(f"""
    INSERT INTO fin_members (first_name, last_name, email, phone_number, date_of_birth)
    VALUES (%s, %s, %s, %s, %s);
    """, (first_name,last_name, email, phone_number, date_of_birth))
    connection.commit()
    #id = cursor.fetchone()[0]
    print("Record inserted successfully!")


def retrieve_members(connection, email=None):
    cursor = connection.cursor()
    if(email is None):
        query = "SELECT * FROM fin_members;"
    else:
        query = "SELECT * FROM fin_members where email = %s ;"
    cursor.execute(query,(email,))
    rows = cursor.fetchall()
    connection.commit()
    for row in rows:
        print(row)
    return rows


def update_member(connection, member_id, first_name, last_name):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE fin_members
    SET first_name = %s, last_name = %s
        WHERE id = %s;
    """, (first_name, last_name, member_id))
    connection.commit()
    print("Record updated successfully!")
    print("updated data")
    retrieve_members(connection, member_id)


def delete_member(connection, member_id):
    cursor = connection.cursor()
    cursor.execute(f"""
    DELETE FROM fin_members
    WHERE id = {member_id};
    """)
    connection.commit()
    print("Record deleted successfully!")