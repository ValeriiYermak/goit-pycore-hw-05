import sys
from collections import defaultdict

# Функція для парсингу рядка логу
def parse_log_line(line: str) -> dict:
    parts = line.split(' ', 3)  # Розділяємо на 4 частини: дата, час, рівень, повідомлення
    if len(parts) < 4:
        return {}
    return {
        'date': parts[0],
        'time': parts[1],
        'level': parts[2],
        'message': parts[3].strip()
    }

# Функція для завантаження логів з файлу
def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                log = parse_log_line(line)
                if log:
                    logs.append(log)
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)
    return logs

# Функція для фільтрації логів за рівнем
def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log['level'].upper() == level.upper()]

# Функція для підрахунку записів за рівнем логування
def count_logs_by_level(logs: list) -> dict:
    counts = defaultdict(int)
    for log in logs:
        counts[log['level']] += 1
    return counts

# Функція для виведення статистики по кількості записів для кожного рівня
def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<15} | {'Кількість':<8}")
    print("-" * 30)
    for level, count in sorted(counts.items()):
        print(f"{level:<15} | {count:<8}")

# Основна функція для обробки логів
def main():
    if len(sys.argv) < 2:
        print("Вкажіть шлях до файлу логів як перший аргумент.")
        sys.exit(1)

    file_path = sys.argv[1]
    logs = load_logs(file_path)

    if len(sys.argv) == 3:
        level = sys.argv[2]
        filtered_logs = filter_logs_by_level(logs, level)
        counts = count_logs_by_level(logs)
        display_log_counts(counts)

        if filtered_logs:
            print(f"\nДеталі логів для рівня '{level.upper()}':")
            for log in filtered_logs:
                print(f"{log['date']} {log['time']} - {log['message']}")
        else:
            print(f"Записів рівня {level.upper()} не знайдено.")
    else:
        counts = count_logs_by_level(logs)
        display_log_counts(counts)

if __name__ == "__main__":
    main()
