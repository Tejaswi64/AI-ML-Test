
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
    elif(table_name == 'accounts'):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id SERIAL PRIMARY KEY,
            member_id int not null,
            branch_id int not null,
            balance float not null,
            account_type VARCHAR(20) NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (member_id) REFERENCES fin_members(member_id) ON DELETE CASCADE,
            FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE SET NULL
        );
        """)
    elif(table_name == 'transactions'):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id SERIAL PRIMARY KEY,
            member_id INT NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            account DECIMAL(10,2) NOT NULL,
            transaction_type VARCHAR(50) check (transaction_type IN ('deposit', 'withdrawal', 'payment', 'refund')),
            description TEXT,
            FOREIGN KEY (member_id) REFERENCES fin_members(member_id) on DELETE CASCADE
        );
        """)
    elif(table_name == 'branch'):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS branch (
            branch_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            street1 VARCHAR(255),
            city VARCHAR(100),
            zip VARCHAR(10)
        );
        """)
    connection.commit()
    print("Table created successfully!")

def db_connection():
            import os
            from dotenv import load_dotenv
            import psycopg2

            # Load environment variables from .env file
            load_dotenv()

            # Database connection setup
            try:
                connection = psycopg2.connect(
                    dbname=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT'),
                    sslmode="require"
                )
                print("Database connection successful!")
                return connection
            except Exception as e:
                print("Error connecting to the database",e)


conn = db_connection()
if conn:
    create_table(conn, 'member')
    create_table(conn, 'branch')
    create_table(conn, 'accounts')
    create_table(conn, 'transactions')
    conn.close()