import time
from functools import wraps

def execution_time_decorator(func):
    """
    Decorator để đo thời gian thực thi của một hàm.

    Args:
        func (function): Hàm cần đo thời gian thực thi.

    Returns:
        function: Hàm bọc lại, kèm tính năng đo thời gian.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Bắt đầu đo thời gian
        result = func(*args, **kwargs)  # Gọi hàm chính
        end_time = time.time()  # Kết thúc đo thời gian
        elapsed_time = end_time - start_time  # Tính thời gian thực thi
        print(f"Execution time for {func.__name__}: {elapsed_time:.4f} seconds")
        return result  # Trả về kết quả của hàm chính

    return wrapper
