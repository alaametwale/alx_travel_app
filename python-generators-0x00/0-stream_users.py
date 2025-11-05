#!/usr/bin/python3
import mysql.connector


def stream_users():
    """Generator to stream users from the database one by one"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
