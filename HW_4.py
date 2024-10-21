"""
Доробіть консольного бота помічника з попереднього домашнього завдання та додайте обробку помилок за допомоги декораторів.

Вимоги до завдання:
Всі помилки введення користувача повинні оброблятися за допомогою декоратора input_error. Цей декоратор відповідає за
повернення користувачеві повідомлень типу "Enter user name", "Give me name and phone please" тощо.
Декоратор input_error повинен обробляти винятки, що виникають у функціях - handler і це винятки: KeyError, ValueError,
IndexError. Коли відбувається виняток декоратор повинен повертати відповідну відповідь користувачеві. Виконання програми
при цьому не припиняється.
"""

import re


def parse_input(user_input):
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]  # Отримати всі аргументи як плоский список
    return cmd, args


def normalize_phone(phone_number):  # Нормалізація номера
    normalized_number = re.sub(r'[^\d+]', '', phone_number)  # Видаляємо всі символи, які не є цифрами

    if normalized_number.startswith('+'):
        if normalized_number.startswith('+380'):
            return normalized_number
        elif normalized_number.startswith('+38'):
            return normalized_number
        elif normalized_number.startswith('+0'):
            return '+38' + normalized_number[2:]
        else:
            return normalized_number
    elif normalized_number.startswith('0'):
        normalized_number = '+38' + normalized_number[1:]
    elif normalized_number.startswith('380'):
        normalized_number = '+' + normalized_number[2:]
    else:
        normalized_number = '+38' + normalized_number
    return normalized_number


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Error: Input all required arguments."

    return inner


@input_error  # Декоратор для обробки помилок
def add_contact(args, contacts):  # Функція для додавання контакту
    if len(args) < 2:  # Перевірка наявності аргументів
        raise ValueError
    name, phone = args
    if name in contacts:
        return "Error: Contact already exists."
    normalized_phone = normalize_phone(phone)  # Нормалізація номера
    contacts[name] = normalized_phone
    save_contacts(contacts)  # Зберігаємо контакти у файл
    return "Contact added."


@input_error
def change_contact(args, contacts):  # Функція для зміни контакту
    if len(args) < 2:  # Перевірка наявності аргументів
        raise ValueError
    name, new_phone = args
    if name not in contacts:
        raise KeyError  # Перевірка наявності імені
    normalized_phone = normalize_phone(new_phone)  # Нормалізація нового номера
    contacts[name] = normalized_phone
    save_contacts(contacts)  # Зберігаємо контакти у файл
    return "Contact updated."


@input_error  # Декоратор для обробки помилок
def show_phone(args, contacts):  # Функція для виведення номера
    if len(args) == 0:
        raise IndexError  # Перевірка наявності аргументів

    name = args[0]
    if name in contacts:
        return contacts[name]
    else:
        raise KeyError  # Перевірка наявності імені


@input_error  # Декоратор для обробки помилок
def show_all(contacts):  # Функція для виведення всіх контактів
    if contacts:
        return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
    else:
        return "No contacts found."


def get_contact_info(path):  # Функція для зчитування контактів з файлу
    contacts = {}
    try:
        with open(path, "r") as file:  # Читаємо контакти з файлу
            for line in file:
                contact_name, contact_phone = line.strip().split(",")  # Розділяємо контакти
                contacts[contact_name.strip()] = contact_phone.strip()  # Записуємо контакти
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return contacts


def save_contacts(contacts, path="contacts_info.txt"):  # Функція для збереження контактів у файл
    # Зберігаємо контакти у файл
    try:
        with open(path, "w") as file:
            for name, phone in contacts.items():
                file.write(f"{name.strip()}, {phone.strip()}\n")  # Записуємо контакти у файл
    except Exception as e:
        print(f"Error saving contacts: {e}")


def main():  # Головна функція для запуску програми
    contacts = {}
    path_to_file = "contacts_info.txt"  # Шлях до файлу з контактами

    try:
        contacts_info = get_contact_info(path_to_file)  # Зчитуємо контакти з файлу
        for contact_name, contact_phone in contacts_info.items():  # Записуємо контакти
            contacts[contact_name] = contact_phone  # Записуємо контакти
    except FileNotFoundError:
        print(f"File '{path_to_file}' not found. Starting with empty contacts.")

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)  # Змінено на плоский список аргументів

        if command in ["close", "exit"]:  # Закриваємо програму
            print("Good bye!")
            break
        elif command == "hello":  # Привітання
            print("How can I help you?")
        elif command == "add":  # Додавання контакту
            print(add_contact(args, contacts))
        elif command == "change":  # Зміна контакту
            if len(args) < 2:  # Перевірка наявності аргументів
                print("Error: Input both name and new phone number.")
            else:
                print(change_contact(args, contacts))
        elif command == "phone":  # Вивід номера з контакту
            if not args:
                print("Error: Input a name.")
            else:
                print(show_phone(args, contacts))
        elif command == "all":  # Вивід всіх контактів
            print(show_all(contacts))  # Виводимо всі контакти
        else:
            print("Invalid command.")


if __name__ == "__main__":  # Запускаємо програму
    main()