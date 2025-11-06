#!/usr/bin/python3
stream_users_in_batches = __import__('1-batch_processing').stream_users_in_batches

# Print the first 2 batches of 5 users
for batch in stream_users_in_batches(batch_size=5):
    print("New Batch:")
    for user in batch:
        print(user)
    print()
