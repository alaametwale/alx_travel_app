#!/usr/bin/python3
import asyncio
import mysql.connector
from mysql.connector import Error


async def fetch_user_data(user_id):
    """Fetch single user data asynchronously"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data WHERE id = %s;", (user_id,))
        result = cursor.fetchone()
        await asyncio.sleep(0.2)  # simulate async delay
        return result

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


async def fetch_multiple_users(user_ids):
    """Fetch multiple users concurrently"""
    tasks = [fetch_user_data(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return results
