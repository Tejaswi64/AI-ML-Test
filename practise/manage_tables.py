
def create_table(connection, table_name):
    cursor = connection.cursor()
    if(table_name == 'members'):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fin_members (
            member_id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone_number VARCHAR(15) UNIQUE,
            date_of_birth DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    elif(table_name == 'transactions'):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fin_member_transactions (
            transaction_id SERIAL PRIMARY KEY,
            member_id INT NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            account DECIMAL(10,2) NOT NULL,
            transaction_type VARCHAR(50) check (transaction_type IN ('deposit', 'withdrawal', 'payment', 'refund')),
            description TEXT,
            FOREIGN KEY (member_id) REFERENCES fin_members(member_id) on DELETE CASCADE
        );
        """)
    connection.commit()
    print("Table created successfully!")