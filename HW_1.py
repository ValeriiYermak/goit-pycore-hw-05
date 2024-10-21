"""
Замикання в програмуванні - це функція, яка зберігає посилання на змінні зі свого лексичного контексту, тобто з області,
де вона була оголошена.Реалізуйте функцію caching_fibonacci, яка створює та використовує кеш для зберігання і повторного
використання вже обчислених значень чисел Фібоначчі.
Ряд Фібоначчі - це послідовність чисел виду: 0, 1, 1, 2, 3, 5, 8, ..., де кожне наступне число послідовності виходить
додаванням двох попередніх членів ряду.
У загальному вигляді для обчислення n-го члена ряду Фібоначчі потрібно вирахувати вираз:Fn=Fn−1+Fn−2Fn−1 =Fn−1+Fn−2.
Це завдання можна вирішити рекурсивно, викликаючи функцію, що обчислює числа послідовності доти, доки виклик не сягне
членів ряду менше n = 1, де послідовність задана.
"""


# Отримуємо функцію fibonacci
def caching_fibonacci():
    cache = {} # Створюємо словник для збереження значень
    # Функція для обчислення числа Фібоначчі
    def fibonacci(n):
        if n <= 0:  # Перевіряємо вхідні дані
            return 0
        if n == 1:  # Перевіряємо вхідні дані
            return 1
        if n in cache: # Перевіряємо вхідні дані
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2) # Запам'ятовуємо значення
        return cache[n]
    return fibonacci # Повертаємо функцію

# Використовуємо функцію fibonacci для обчислення чисел
fib = caching_fibonacci() # Повертаємо функцію
print(fib(10))
print(fib(15))