import time
import multiprocessing
import os

def measure_execution_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

def factorize_sync(*numbers):
    results = []
    for number in numbers:
        factors = []
        for i in range(1, number + 1):
            if number % i == 0:
                factors.append(i)
        results.append(factors)
    return results

def factorize_number(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(*numbers):
    with multiprocessing.Pool() as pool:
        results = pool.map(factorize_number, numbers)
    
    return results

if __name__ == "__main__":
    # Тестові дані
    test_numbers = (128, 255, 99999, 10651060)

    # Вимірюємо час для синхронної версії
    sync_result, sync_time = measure_execution_time(factorize_sync, *test_numbers)
    print(f"Синхронна версія: Виконано за {sync_time:.4f} секунд")

    # Вимірюємо час для паралельної версії
    parallel_result, parallel_time = measure_execution_time(factorize_parallel, *test_numbers)
    print(f"Паралельна версія: Виконано за {parallel_time:.4f} секунд")

    # Перевірка результатів
    a, b, c, d = parallel_result

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print("Результати перевірки вірності: усі тести пройдено успішно.")
