#!/usr/bin/python3
"""
Task 2: Implement a generator to group streamed data into batches.
File: 1-batch_processor.py
Prototype: def batch_stream(generator, batch_size)
"""
from typing import Generator, List, Any

# هذه الدالة لا تحتاج لاستيراد stream_users بشكل مباشر، 
# لكنها مصممة لكي تستقبل أي مولد كمدخل (Input Generator).

def batch_stream(generator: Generator[Any, None, None], batch_size: int) -> Generator[List[Any], None, None]:
    """
    دالة مولدة تأخذ تدفق بيانات (مولد) وتقوم بتجميع العناصر في دفعات (Lists)
    بحجم محدد (batch_size).

    Args:
        generator: المولد المصدر الذي ينتج عناصر فردية (مثل stream_users()).
        batch_size: الحد الأقصى لحجم الدفعة.

    Yields:
        List[Any]: قائمة تحتوي على دفعة من العناصر.
    """
    
    if batch_size <= 0:
        raise ValueError("Batch size must be a positive integer.")
        
    batch = []
    
    # 1. التكرار على المولد المصدر
    for item in generator:
        batch.append(item)
        
        # 2. فحص ما إذا كانت الدفعة قد امتلأت
        if len(batch) == batch_size:
            # إرجاع الدفعة المكتملة باستخدام yield
            yield batch
            # إعادة تعيين الدفعة لبدء الدفعة التالية
            batch = []
    
    # 3. إرجاع أي عناصر متبقية كدفعة نهائية (قد تكون جزئية)
    if batch:
        yield batch


if __name__ == '__main__':
    # مثال توضيحي: لكي يعمل هذا المثال، يجب أن يكون لديك ملف 0-stream_users.py
    # الذي يحتوي على الدالة stream_users().
    try:
        from 0_stream_users import stream_users

        TEST_BATCH_SIZE = 3
        print(f"--- بدء معالجة الدفعات بحجم: {TEST_BATCH_SIZE} ---")
        
        # استهلاك المولد الجديد
        batch_generator = batch_stream(stream_users(), TEST_BATCH_SIZE)
        
        for i, batch in enumerate(batch_generator):
            print(f"\n✅ تم جلب الدفعة رقم {i+1} (حجم: {len(batch)})")
            
            # طباعة IDs الدفعة للتحقق
            for user in batch:
                print(f"  - User ID: {user['user_id'][-8:]}, Age: {user['age']}")
            
            if i >= 1: # إيقاف بعد دفعتين للعرض
                break
                
    except ImportError:
        print("\n[!] فشل الاستيراد: تأكد من وجود ملف 0-stream_users.py.")
    except Exception as e:
        print(f"\n[!] حدث خطأ أثناء التشغيل: {e}")