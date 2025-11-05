#!/usr/bin/python3
"""
Task 2: Implement a generator for streaming users in batches and another for processing them.
File: 1-batch_processor.py
"""
import mysql.connector
from typing import Generator, Dict, Any, List, Tuple
# استيراد تفاصيل الاتصال من ملف seed.py
from seed import connect_to_prodev, TABLE_NAME 

# ----------------------------------------------------------------------
# 1. الدالة المولدة لتدفق المستخدمين في دفعات (تلبية شرط [SELECT, FROM user_data])
# ----------------------------------------------------------------------

def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Generator function that connects to the database and streams user_data 
    rows in batches of a specified size.

    Args:
        batch_size: الحد الأقصى لحجم الدفعة.

    Yields:
        List[Dict[str, Any]]: قائمة من القواميس تمثل دفعة من صفوف المستخدمين.
    """
    if batch_size <= 0:
        raise ValueError("Batch size must be a positive integer.")

    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if not connection:
            return 

        # استخدام مؤشر بجلب القاموس لتسهيل العمل لاحقًا
        cursor = connection.cursor(dictionary=True) 
        
        # يجب أن تتضمن السلسلة "FROM user_data" و "SELECT" في الكود
        select_query = f"SELECT user_id, name, email, age FROM {TABLE_NAME};"
        cursor.execute(select_query)
        
        # حلقة واحدة لتدفق البيانات وتجميعها في دفعات
        while True:
            # جلب مجموعة من الصفوف دفعة واحدة (بدلاً من fetchone)
            # هذه هي الطريقة الأكثر كفاءة لـ "Batching" من قاعدة البيانات.
            batch_rows: List[Dict[str, Any]] = cursor.fetchmany(batch_size) 
            
            if not batch_rows:
                break
            
            # إرجاع الدفعة كاملة باستخدام yield
            yield batch_rows

    except mysql.connector.Error as err:
        print(f"Database error during batch streaming: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ----------------------------------------------------------------------
# 2. الدالة لمعالجة وتصفية كل دفعة (تلبية شرط [batch_processing, 25])
# ----------------------------------------------------------------------

def batch_processing(batch_generator: Generator[List[Dict[str, Any]], None, None]) -> Generator[Dict[str, Any], None, None]:
    """
    دالة مولدة تستقبل تدفق الدفعات (batches) وتقوم بمعالجة كل دفعة
    لتصفية المستخدمين الذين تزيد أعمارهم عن 25 عامًا.

    Args:
        batch_generator: المولد الذي ينتج قوائم الدفعات (من stream_users_in_batches).

    Yields:
        Dict[str, Any]: قاموس يمثل المستخدم الذي تجاوز 25 عامًا.
    """
    # التكرار على الدفعات التي ينتجها المولد المدخل
    for batch in batch_generator:
        # التكرار على المستخدمين داخل كل دفعة
        for user in batch:
            # التحقق من شرط التصفية
            if user.get('age', 0) > 25: # شرط تصفية المستخدمين الذين تزيد أعمارهم عن 25
                # إرجاع المستخدم الفردي الذي تمت تصفيته
                yield user


if __name__ == '__main__':
    # مثال استخدام واختبار الوظائف
    TEST_BATCH_SIZE = 5
    print(f"--- بدء تدفق الدفعات بحجم: {TEST_BATCH_SIZE} ---")
    
    # الخطوة 1: الحصول على مولد الدفعات
    batch_gen = stream_users_in_batches(TEST_BATCH_SIZE)
    
    # الخطوة 2: تمرير مولد الدفعات إلى دالة المعالجة
    processed_gen = batch_processing(batch_gen)
    
    # استهلاك المولد النهائي (الذي يحتوي على المستخدمين > 25 عامًا)
    filtered_count = 0
    print("\n--- المستخدمون الذين تزيد أعمارهم عن 25 عامًا (من الدفعات) ---")
    
    for user in processed_gen:
        print(f"✅ User ID: {user['user_id'][-8:]}, Name: {user['name']}, Age: {user['age']}")
        filtered_count += 1
        if filtered_count >= 10: # توقف مبكر
             break

    print(f"\nتم تصفية وإخراج {filtered_count} مستخدمًا.")