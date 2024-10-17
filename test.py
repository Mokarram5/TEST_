import mysql.connector
from mysql.connector import Error
import os

def create_connection(host, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error occurred: {e}")
        return None
    
def create_database(connection, db_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()

def create_table(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                status VARCHAR(255) NOT NULL,
                origin VARCHAR(255) NOT NULL
            )
            """)
        print(f"Table '{table_name}' created or already exists.")
        
        # Insert sample data
        cursor.execute(f"INSERT INTO {table_name} (status, origin) VALUES (%s, %s)", ('checked', 'Asia'))
        cursor.execute(f"INSERT INTO {table_name} (status, origin) VALUES (%s, %s)", ('checked', 'Europe'))
        connection.commit()

        # Update data
        cursor.execute(f"UPDATE {table_name} SET status = 'unchecked' WHERE origin = 'Asia'")
        connection.commit()

        # Delete data
        cursor.execute(f"DELETE FROM {table_name} WHERE origin = 'Europe'")
        connection.commit()

        # Fetch data
        cursor.execute(f"SELECT * FROM {table_name}")
        results = cursor.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()

def connect_to_database(connection, db_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {db_name}")
        print(f"Connected to database '{db_name}'")
        return cursor
    except Error as e:
        print(f"Error occurred: {e}")
        return None
    
# Main execution
conn = create_connection("localhost", "root", "pwskills")
if conn:
    create_database(conn, "mavenfuzzyfactory")

    db_Conn = connect_to_database(conn, "mavenfuzzyfactory")

    if db_Conn:
        create_table(conn, "Data")  # Create table and manipulate data
        db_Conn.close()  # Close the cursor

    conn.close()  # Close the connection to the server