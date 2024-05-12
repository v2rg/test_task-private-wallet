"""
Основные возможности:
1. Вывод баланса: Показать текущий баланс, а также отдельно доходы и расходы.
2. Добавление записи: Возможность добавления новой записи о доходе или расходе.
3. Редактирование записи: Изменение существующих записей о доходах и расходах.
4. Поиск по записям: Поиск записей по категории, дате или сумме.
"""
import datetime
import json


class PrivateWallet:
    def create_wallet(self, new_wallet) -> None:  # создаем файл
        with open('wallet.json', 'w', encoding='utf-8') as f:
            wallet = json.dumps(
                {
                    'balance': (
                        new_wallet['total_sum'] if new_wallet['operation'] == 'доход' else new_wallet['total_sum'] * -1
                    ),
                    'entries': [new_wallet]
                }, indent=4, default=str
            )
            f.write(wallet)

    def read_from_file(self) -> (bool, dict):  # получаем данные из файла
        try:
            with open('wallet.json', encoding='utf-8') as f:
                wallet = json.load(f)
        except (ValueError, FileNotFoundError):
            return False
        else:
            if isinstance(wallet, dict):
                try:
                    _ = wallet['balance']
                    _ = wallet['entries']
                except KeyError:
                    return False
                else:
                    return wallet
            else:
                print('\n- Ошибка в файле')

    def rewrite_file(self, updated_wallet) -> None:  # перезаписываем файл
        with open('wallet.json', 'w', encoding='utf-8') as f:
            json.dump(updated_wallet, f, indent=4, default=str, ensure_ascii=False)

    def show_finance(self):  # вывод финансовой информации
        def finance_method(operation) -> float:  # получаем баланс, доход, расход
            if operation == 'доход':
                return sum(x['total_sum'] for x in wallet['entries'] if x['operation'] == 'доход')
            elif operation == 'расход':
                return sum(x['total_sum'] for x in wallet['entries'] if x['operation'] == 'расход') * -1
            elif operation == 'balance':
                return wallet['balance']

        wallet = self.read_from_file()

        if wallet:
            while True:
                print(
                    "\n===== Финансы ====="
                    "\n1) Баланс"
                    "\n2) Доход"
                    "\n3) Расход"
                    "\n0) Вернуться в главное меню"
                )

                user_action_finance = input('\nВведите номер операции: ')

                try:
                    user_action_finance = int(user_action_finance)
                except ValueError:
                    continue
                else:
                    if user_action_finance == 1:
                        input(f"\n- Баланс: {finance_method('balance')}")
                        continue
                    elif user_action_finance == 2:
                        input(f"\n- Доход: {finance_method('доход')}")
                        continue
                    elif user_action_finance == 3:
                        input(f"\n- Расход: {finance_method('расход')}")
                        continue
                    elif user_action_finance == 0:
                        break
        else:
            input('\nОшибка в файле...')

    def add_entry(self):  # добавляем запись в кошелек
        wallet = self.read_from_file()

        def user_input_date() -> (str, None):  # ввод даты операции
            while True:
                date = input("\nВведите дату (в формате '2024-05-11' или 'текущая' или q): ")

                if date == 'q':
                    return
                elif date == 'текущая':
                    date = datetime.datetime.now()
                    print(f"\n- Текущая дата {date}")

                    confirm_date = input('\nПодтвердите ввод даты (y/n): ').lower()

                    if confirm_date == 'y':
                        return date
                    elif confirm_date == 'n':
                        continue

                else:
                    try:
                        date = [int(x) for x in date.split('-')]
                        date = datetime.datetime(*date, microsecond=True)
                    except (ValueError, TypeError):
                        print('\n- Некорректная дата')
                        continue
                    else:
                        confirm_date = input('Подтвердите ввод даты (y/n): ').lower()
                        if confirm_date == 'y':
                            return date
                        elif confirm_date == 'n':
                            continue

        def user_input_operation():  # ввод типа операции
            while True:
                operation = input('\nВведите операцию (доход/расход или q): ').lower()

                if operation == 'q':
                    return
                elif operation == 'доход':
                    break
                elif operation == 'расход':
                    break

            return operation

        def user_input_total_sum():  # ввод суммы
            while True:
                total_sum = input('\nВведите сумму (1500/758.54 или q): ')

                if total_sum == 'q':
                    return
                try:
                    total_sum = float(total_sum)
                except ValueError:
                    print('Можно вводить только цифры')
                    continue
                else:
                    confirm_total_sum = input('Подтвердите ввод суммы (y/n): ').lower()
                    if confirm_total_sum == 'y':
                        break
                    elif confirm_total_sum == 'n':
                        continue

            return total_sum

        def user_input_description():  # ввод описания
            while True:
                description = input('\nВведите описание (q - отмена): ')

                if description == 'q':
                    return
                else:
                    confirm_description = input('Подтвердите ввод описания (y/n): ').lower()

                    if confirm_description == 'y':
                        break
                    elif confirm_description == 'n':
                        continue

            return description

        print('\n\n===== Добавление записи =====')

        date = user_input_date()

        if date:
            operation = user_input_operation()
            if operation:
                total_sum = user_input_total_sum()
                if total_sum:
                    description = user_input_description()
                    if description:

                        if wallet:  # id записи
                            entry_id = wallet['entries'][-1]['id'] + 1
                        else:
                            entry_id = 1

                        result = {
                            'id': entry_id,
                            'date': date,
                            'operation': operation,
                            'total_sum': total_sum,
                            'description': description
                        }

                        print(
                            f"\n\n--- Проверка новой записи\n"
                            f"\nДата: {datetime.datetime.strftime(result['date'], '%Y-%m-%d %H:%M:%S')}"
                            f"\nОперация: {result['operation']}"
                            f"\nСумма: {result['total_sum']}"
                            f"\nОписание: {result['description']}"
                        )  # проверка новой записи

                        confirmation = str(input('\nПодтвердите ввод (y/n): ')).lower()  # подтверждение

                        if confirmation == 'y':
                            if wallet:
                                wallet['entries'].append(result)
                                wallet['balance'] = (
                                    wallet['balance'] + total_sum
                                    if operation == 'доход'
                                    else wallet['balance'] - total_sum
                                )

                                self.rewrite_file(wallet)  # сохраняем измененные данные в файл (если он существует)
                                input('\n--- Запись добавлена')
                            else:
                                self.create_wallet(
                                    result)  # создаем новый файл и сохраняем в него запись (если файла нет)
                                input('\n--- Файл создан, запись добавлена')
                        else:
                            return
                    else:
                        input('\nОтмена...')
                else:
                    input('\nОтмена...')
            else:
                input('\nОтмена...')
        else:
            input('\nОтмена...')

    def edit_entry(self):  # редактирование записи
        wallet = self.read_from_file()

        if wallet:
            def count_entries_1() -> int:  # возвращает кол-во записей
                return len(wallet['entries'])

            def list_entries_2() -> None:  # выводит список записей (desc)
                if count_entries_1():
                    count = 2  # количество выводимых записей
                    for i in wallet['entries'][::-1]:
                        count -= 1
                        # yield f"{i['id']} | {i['date']} | {i['operation']} | {i['total_sum']} | {i['description']}"
                        print(f"{i['id']} | {i['date']} | {i['operation']} | {i['total_sum']} | {i['description']}")
                        if count == 0:
                            count = 2
                            input('...')
                    input('\n\nЗаписей больше нет...')
                else:
                    input('\n\nЗаписей нет...')

            def edit_entry_3():  # редактирует запись
                def current_entry_str(entry_id) -> str:  # возвращает текущую запись в виде str
                    current_entry = [x for x in wallet['entries'] if x['id'] == entry_id]
                    if current_entry:
                        current_entry = current_entry[0]
                        current_entry_str = (
                            f"\nid: {current_entry['id']}"
                            f"\nДата: {current_entry['date']}"
                            f"\nОперация: {current_entry['operation']}"
                            f"\nСумма: {current_entry['total_sum']}"
                            f"\nОписание: {current_entry['description']}"
                        )

                        return current_entry_str

                def change_date() -> bool:  # изменяет дату текущей записи
                    while True:
                        user_new_date = input('\nВведите новую дату (в формате 2024-02-17 или q): ')

                        if user_new_date == 'q':
                            break
                        else:
                            try:
                                user_new_date = [int(x) for x in user_new_date.split('-')]
                                user_new_date = datetime.datetime(*user_new_date, microsecond=True)
                            except (ValueError, TypeError):
                                print('\n- Некорректная дата')
                                continue
                            else:
                                user_action_new_date = input(f"\nПодтвердите новую дату '{user_new_date}' (y/n): ")

                                if user_action_new_date == 'n':
                                    break
                                elif user_action_new_date == 'y':
                                    current_entry['date'] = user_new_date
                                    self.rewrite_file(wallet)
                                    input('\n- Дата изменена...')

                                    return True
                    return False

                def change_operation() -> bool:  # изменяет тип операции для текущей записи
                    while True:
                        user_new_operation = input('\nВведите новый тип операции (доход/расход или q): ').lower()

                        if user_new_operation == 'q':
                            break
                        elif user_new_operation in ('доход', 'расход'):
                            while True:
                                user_action_new_operation = input(
                                    f"\nПодтвердите изменение операции '{user_new_operation}' (y/n): ")
                                if user_action_new_operation == 'n':
                                    break
                                elif user_action_new_operation == 'y':
                                    current_entry['operation'] = user_new_operation
                                    self.rewrite_file(wallet)
                                    input('\n- Операция изменена...')

                                    return True
                    return False

                def change_sum():  # изменяет сумму для текущей записи
                    while True:
                        user_new_sum = input('\nВведите новую сумму (1500/125.2 или q): ')

                        if user_new_sum == 'q':
                            break
                        else:
                            try:
                                user_new_sum = float(user_new_sum)
                            except ValueError:
                                continue
                            else:
                                user_action_new_sum = input(
                                    f"\nПодтвердите изменение суммы '{user_new_sum}' (y/n): ")
                                if user_action_new_sum == 'n':
                                    break
                                elif user_action_new_sum == 'y':
                                    current_entry['total_sum'] = user_new_sum
                                    self.rewrite_file(wallet)
                                    input('\n- Сумма изменена...')

                                    return True

                    return False

                def change_description():  # изменяет описание для текущей записи
                    while True:
                        user_new_description = input('\nВведите новое описание (или q): ')

                        if user_new_description == 'q':
                            break
                        else:
                            user_action_new_sum = input(
                                f"\nПодтвердите изменение описания '{user_new_description}' (y/n): ")
                            if user_action_new_sum == 'n':
                                break
                            elif user_action_new_sum == 'y':
                                current_entry['description'] = user_new_description
                                self.rewrite_file(wallet)
                                input('\n- Описание изменено...')

                                return True

                    return False

                while True:
                    entry_id = input('\nВведите id записи (число или q): ')

                    if entry_id == 'q':
                        break
                    else:
                        try:
                            entry_id = int(entry_id)
                        except ValueError:
                            continue
                        else:
                            current_entry_string = current_entry_str(entry_id)

                            if current_entry_string:
                                print("\n\n=== Изменяемая запись ===")
                                print(current_entry_string)

                                user_action = input('\nПодтвердить выбор записи (y/n): ')

                                if user_action == 'n':
                                    break
                                else:
                                    while True:
                                        current_entry = [x for x in wallet['entries'] if x['id'] == entry_id][0]
                                        print(
                                            f"\n=== Изменение записи id {current_entry['id']} ==="
                                            f"\n1) Просмотреть запись"
                                            f"\n2) Изменить дату"
                                            f"\n3) Изменить операцию"
                                            f"\n4) Изменить сумму"
                                            f"\n5) Изменить описание"
                                            f"\n0) Вернуться назад"
                                        )

                                        user_action = input('\nВведите номер операции: ')

                                        try:
                                            user_action = int(user_action)
                                        except ValueError:
                                            continue
                                        else:
                                            if user_action == 1:
                                                print('\n\n--- Просмотр редактируемой записи')
                                                print(current_entry_str(entry_id))
                                                input('\n...')

                                            elif user_action == 2:
                                                print('\n\n--- Изменение даты')
                                                print(f"\nТекущая дата '{current_entry['date']}'")
                                                change_date()

                                            elif user_action == 3:
                                                print('\n\n--- Изменение типа операции')
                                                print(f"\nТекущая операция '{current_entry['operation']}'")
                                                change_operation()

                                            elif user_action == 4:
                                                print('\n\n--- Изменение суммы')
                                                print(f"\nТекущая сумма '{current_entry['total_sum']}'")
                                                change_sum()

                                            elif user_action == 5:
                                                print('\n\n--- Изменение описания')
                                                print(f"\nТекущее описание '{current_entry['description']}'")
                                                change_description()

                                            elif user_action == 0:
                                                break
                                break
                            else:
                                print('\n--- Запись не найдена')
                                input('\n...')
                                continue

            if len(wallet['entries']) > 0:
                while True:  # основной цикл
                    print(
                        '\n\n===== Изменение записи ======'
                        '\n1) Количество записей',
                        '\n2) Список всех записей'
                        '\n3) Выбрать запись для редактирования'
                        '\n0) Вернуться в главное меню'
                    )

                    user_action_edit_entry = input('\nВведите номер операции: ')

                    try:
                        user_action_edit_entry = int(user_action_edit_entry)
                    except ValueError:
                        continue
                    else:
                        if user_action_edit_entry == 1:  # вывод кол-ва записей
                            count = count_entries_1()
                            print(f"\n\n--- Всего записей: {count}")
                            input('\n...')

                        elif user_action_edit_entry == 2:  # вывод списка записей (desc)
                            print('\n\n --- Список всех записей')
                            list_entries_2()
                            # input('\n...')

                        elif user_action_edit_entry == 3:  # изменение записи (по id)
                            print('\n\n=== Изменение записи ===')
                            edit_entry_3()

                        elif user_action_edit_entry == 0:
                            break
            else:
                input('\nЗаписей нет...')

        else:
            input('\nЗаписи не найдены...')

    def search(self):  # поиск записи
        wallet = self.read_from_file()

        def show_search_result(method) -> None:
            result = None
            user_search_query = None

            if method == 'date':  # поиск по дате операции
                while True:
                    user_search_query = input('\nВведите дату (в формате 2020-05-01 или q): ')

                    if user_search_query == 'q':
                        break
                    else:
                        result = [x for x in wallet['entries'] if x['date'].startswith(user_search_query)]
                        break

            elif method == 'operation':  # поиск по типу операции
                while True:
                    user_search_query = input('\nВведите тип операции (доход/расход или q): ')

                    if user_search_query == 'q':
                        break
                    else:
                        if user_search_query in ('доход', 'расход'):
                            result = [x for x in wallet['entries'] if x['operation'] == user_search_query]
                            break
                        else:
                            continue

            elif method == 'total_sum':  # поиск по сумме операции
                while True:
                    user_search_query = input('\nВведите сумму (1300/430.5 или q): ')

                    if user_search_query == 'q':
                        break
                    else:
                        try:
                            user_search_query = float(user_search_query)
                        except ValueError:
                            continue
                        else:
                            result = [x for x in wallet['entries'] if x['total_sum'] == user_search_query]
                            break

            else:
                print('\n- Метод не найден')
                print('\n...')

            if user_search_query == 'q':
                ...
            else:
                if result:
                    length = len(result)
                    input(f"\nНайдено: {length} ...")

                    for i in range(length):
                        current_entry = result[i]

                        print(f"{current_entry['id']} | "
                              f"{current_entry['date']} | "
                              f"{current_entry['operation']} | "
                              f"{current_entry['total_sum']} | "
                              f"{current_entry['description']}")

                        try:
                            result[i + 1]
                        except IndexError:
                            input('\nБольше нет...')
                        else:
                            input('...')

                else:
                    input('\nНичего не найдено...')

        if wallet:
            if len(wallet['entries']) > 0:
                while True:
                    print(
                        "\n\n=== Поиск ==="
                        "\n1) По дате"
                        "\n2) По операции"
                        "\n3) По сумме"
                        "\n0) Вернуться в главное меню"
                    )

                    user_action_search = input('\nВведите номер операции: ')

                    try:
                        user_action_search = int(user_action_search)
                    except ValueError:
                        continue
                    else:
                        if user_action_search == 1:
                            print('\n\n--- Поиск по дате')
                            show_search_result('date')
                        elif user_action_search == 2:
                            print('\n\n--- Поиск по операции')
                            show_search_result('operation')
                        elif user_action_search == 3:
                            print('\n\n--- Поиск по сумме')
                            show_search_result('total_sum')
                        elif user_action_search == 0:
                            break

            else:
                input('\nЗаписей нет...')
        else:
            input('\nОшибка в файле...')

    def main_method(self) -> None:  # основной метод
        main_actions = (
            "\n===== Главная ====="
            "\n1) Финансы"
            "\n2) Добавить запись"
            "\n3) Изменить запись"
            "\n4) Поиск"
            "\n0) Выход"
        )
        while True:
            print(main_actions)

            user_action = input('\nВведите номер операции: ')

            try:
                user_action = int(user_action)
            except ValueError:
                continue
            else:
                if user_action == 1:  # финансы
                    self.show_finance()
                elif user_action == 2:  # добавить запись
                    self.add_entry()
                elif user_action == 3:  # изменить запись
                    self.edit_entry()
                elif user_action == 4:  # поиск
                    self.search()
                elif user_action == 0:
                    break


wallet = PrivateWallet()
wallet.main_method()
