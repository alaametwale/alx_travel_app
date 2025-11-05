#!/usr/bin/python3
import seed

def stream_users_in_batches(batch_size):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    batch = cursor.fetchmany(batch_size)
    while batch:
        yield batch
        batch = cursor.fetchmany(batch_size)
    cursor.close()
    connection.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
