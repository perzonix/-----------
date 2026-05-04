import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

def load_expenses():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_expenses(expenses):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)
        
def add_expense(expenses):
    print("\n--- Добавление новой траты ---")
    try:
        amount = float(input("Введите сумму расхода: "))
        if amount <= 0:
            print("Ошибка: Сумма должна быть положительной")
            return
    except ValueError:
        print("Ошибка: Введите корректное число")
        return

    category = input("Введите категорию (еда, транспорт и т.д.): ").strip()
    if not category:
        print("Ошибка: Категория не может быть пустой")
        return

    date_input = input("Введите дату (ДД.ММ.ГГГГ) или Enter для сегодняшней: ").strip()
    if date_input:
        try:
            date_obj = datetime.strptime(date_input, "%d.%m.%Y")
            date = date_obj.strftime("%d.%m.%Y")
        except ValueError:
            print("Ошибка: Неверный формат даты.")
            return
    else:
        date = datetime.now().strftime("%d.%m.%Y")

    new_expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "category": category,
        "date": date
    }

    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Успешно добавлено! {amount} руб. в категорию '{category}'")
    
def filter_by_date(expenses):
    print("\n--- Фильтр по дате ---")
    if not expenses:
        print("Нет записей о расходах")
        return

    date_input = input("Введите дату для фильтрации (ДД.ММ.ГГГГ): ").strip()
    try:
        filter_date = datetime.strptime(date_input, "%d.%m.%Y").strftime("%d.%m.%Y")
    except ValueError:
        print("Ошибка: Неверный формат даты.")
        return

    filtered = [e for e in expenses if e["date"] == filter_date]
    if not filtered:
        print(f"На дату {filter_date} расходов не найдено")
        return

    print(f"\nРасходы за {filter_date}:")
    total = 0
    for expense in filtered:
        print(f"  Категория: {expense['category']}, Сумма: {expense['amount']} руб.")
        total += expense['amount']
    print(f"Итого за день: {total:.2f} руб.")

def filter_by_category(expenses):
    print("\n--- Фильтр по категории ---")
    if not expenses:
        print("Нет записей о расходах")
        return
    
    categories = sorted(set(expense["category"] for expense in expenses))
    print("Доступные категории:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    category = input("\nВведите название категории: ").strip()
    filtered = [e for e in expenses if e["category"].lower() == category.lower()]

    if not filtered:
        print(f"В категории '{category}' расходов не найдено")
        return

    print(f"\nРасходы в категории '{category}':")
    total = 0
    for expense in filtered:
        print(f"  Дата: {expense['date']}, Сумма: {expense['amount']} руб.")
        total += expense['amount']
    print(f"Итого в категории: {total:.2f} руб.")
    
def show_all_expenses(expenses):  
    print("\n--- Все расходы ---")
    if not expenses:
        print('Нет записей о расходах')
        return
    for i, expns in enumerate(expenses, 1):
        print(f"{i}. Категория: {expns['category']}, Сумма: {expns['amount']}, Дата: {expns['date']}")
    
def filter_expenses(expenses):    
    print("1. По дате\n2. По категории")
    choice = input('Выберите действие: ')
    if choice == '1':
        filter_by_date(expenses)
    elif choice == '2':
        filter_by_category(expenses)   
    
def delete_expense(expenses):
    show_all_expenses(expenses) 
    if not expenses:
        return 
    try:
        index = int(input("Введите номер записи для удаления: "))
        if 1 <= index <= len(expenses):
            removed = expenses.pop(index - 1)
            save_expenses(expenses)
            print(f"Запись '{removed['category']}' удалена.")
        else:
            print("Ошибка: Неверный номер записи.")
    except ValueError:
        print("Ошибка: Введите целое число.")
    
def show_menu():
    print("\n" + "="*40)
    print("УЧЕТ ЕЖЕДНЕВНЫХ РАСХОДОВ")
    print("="*40)
    print("1. Показать все расходы")
    print("2. Добавить новый расход")
    print("3. Фильтровать расходы")
    print("4. Удалить запись")
    print("5. Выйти")
    print("="*40)

def main():
    print("Добро пожаловать в приложение для учета расходов!")
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("\nВыберите действие (1-5): ").strip()

        if choice == "1":
            show_all_expenses(expenses)
        elif choice == "2":
            add_expense(expenses)
        elif choice == "3":
            filter_expenses(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            print("\nДо свидания! Ваши данные сохранены.")
            break
        else:
            print("Ошибка: Неверный выбор.")
            
if __name__ == "__main__":
    main()