# seed.py
# سكربت إعداد قاعدة بيانات ALX_prodev وجداولها وملء بيانات من CSV

import mysql.connector
from mysql.connector import Error
import csv
import uuid
import os

def connect_db():
    """Connect to MySQL server."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345"
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

def create_database(connection):
    """Create database ALX_prodev if not exists."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="ALX_prodev"
        )
        return conn
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection):
    """Create table user_data."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age INT NOT NULL
            );
        """)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

def insert_data(connection, csv_file):
    """Insert data from CSV into user_data."""
    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        return

    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows_inserted = 0
            for row in reader:
                name = row.get('name', '').strip()
                email = row.get('email', '').strip()
                age_raw = row.get('age', '0').strip()
                try:
                    age = int(float(age_raw))
                except:
                    age = 0
                user_id = str(uuid.uuid4())
                try:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )
                    rows_inserted += 1
                except Error as e:
                    print(f"Warning: could not insert row ({name}, {email}, {age}): {e}")
        connection.commit()
        print(f"Data inserted successfully ({rows_inserted} rows)")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()
        print("Initial connection and database creation done.")

        conn2 = connect_to_prodev()
        if conn2:
            create_table(conn2)
            insert_data(conn2, "user_data.csv")

            try:
                cur = conn2.cursor()
                cur.execute("SELECT * FROM user_data LIMIT 5;")
                rows = cur.fetchall()
                print(rows)
            except Exception as e:
                print(f"Error fetching rows: {e}")
            finally:
                cur.close()
            conn2.close()
    else:
        print("Could not connect to MySQL server.")
