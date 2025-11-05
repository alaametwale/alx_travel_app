#!/usr/bin/python3
import seed

def stream_users_in_batches(batch_size):
    """Generator that yields batches of users from the database"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # ✅ هنا بنستخدم yield لتوليد البيانات على دفعات

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Process each batch and print users older than 25"""
    for batch in stream_users_in_batches(batch_size):  # ✅ هنا بنستخدم yield generator
        for user in batch:
            if user['age'] > 25:
                print(user)
