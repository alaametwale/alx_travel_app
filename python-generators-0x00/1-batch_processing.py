#!/usr/bin/python3
import seed

def batch_processing(batch_size):
    """Generator that yields users older than 25 in batches"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        # هنا نفلتر ونرجع المستخدمين الأكبر من 25 سنة
        filtered = [user for user in batch if user['age'] > 25]
        if filtered:
            yield filtered  # ✅ yield هنا داخل batch_processing زي ما ALX عايز

    cursor.close()
    connection.close()
