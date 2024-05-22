import datetime
import json
import os
from unittest import TestCase
from unittest.mock import patch
from unittest import mock

from main import PrivateWallet


class WalletTestCase(TestCase):
    TEST_WALLET = {
        "balance": 500,
        "entries": [
            {
                "id": 1,
                "date": "2024-05-20 00:00:00.00001",
                "operation": "доход",
                "total_sum": 500,
                "description": "test_description"
            }
        ]
    }

    @classmethod
    def setUpClass(self):
        self.wallet = PrivateWallet()

    def tearDown(self):
        if os.path.exists('test_wallet.json'):
            os.remove('test_wallet.json')

    # @classmethod
    # def tearDownClass(cls):  # удаляем тестовый файл
    #     if os.path.exists('test_wallet.json'):
    #         os.remove('test_wallet.json')

    def create_test_file(self):  # создаем тестовый файл
        with open('test_wallet.json', 'w', encoding='utf-8') as f:
            json.dump(self.TEST_WALLET, f, indent=4, default=str, ensure_ascii=False)

    def test_create_wallet_json(self):  # проверка создания файла 'test_wallet.json'

        test_result = {
            'id': 1,
            'date': '2024-05-13 00:00:00.01',
            'operation': 'доход',
            'total_sum': 500,
            'description': 'test_description'
        }

        self.assertEqual(self.wallet.create_wallet(test_result), True)
        self.assertNotEqual(self.wallet.create_wallet(test_result), None)

    def test_read_wallet_json(self):  # проверка содержимого файла 'test_wallet.json'

        self.create_test_file()  # создаем тестовый файл

        read_test_result = {
            "balance": 500,
            "entries": [
                {
                    "id": 1,
                    "date": "2024-05-20 00:00:00.00001",
                    "operation": "доход",
                    "total_sum": 500,
                    "description": "test_description"
                }
            ]
        }

        self.assertIsInstance(self.wallet.read_from_file(), dict)
        self.assertNotEqual(self.wallet.read_from_file(), False)
        self.assertEqual(self.wallet.read_from_file(), read_test_result)

    def test_rewrite_file(self):  # проверка перезаписи файла 'test_wallet.json'

        self.create_test_file()

        rewrite_entry = {
            "balance": 150,
            "entries": [
                {
                    "id": 1,
                    "date": "2000-01-01 00:00:00.01",
                    "operation": "доход",
                    "total_sum": 500,
                    "description": "rewrite_test_description"
                }
            ]
        }

        self.assertEqual(self.wallet.rewrite_file(rewrite_entry), True)
        self.assertIsInstance(self.wallet.read_from_file(), dict)
        self.assertNotEqual(self.wallet.read_from_file(), False)
        self.assertEqual(self.wallet.read_from_file(), rewrite_entry)

    def test_show_finance(self):  # проверка вывода баланса, дохода, расхода из файла 'test_wallet.json'

        self.create_test_file()

        self.assertEqual(self.wallet.finance_method('balance'), 500)  # вывод баланса
        self.assertEqual(self.wallet.finance_method('доход'), 500)  # вывод дохода
        self.assertEqual(self.wallet.finance_method('расход'), 0)  # # вывод расхода

    def test_add_entry(self):  # проверка добавления записи

        self.create_test_file()

        result = {
            'balance': 5500.0,
            'entries': [
                {
                    'date': '2024-05-20 00:00:00.00001',
                    'description': 'test_description',
                    'id': 1,
                    'operation': 'доход',
                    'total_sum': 500
                },
                {
                    'date': '2024-05-16 00:00:00.000001',
                    'description': 'add_entry_test_description',
                    'id': 2,
                    'operation': 'доход',
                    'total_sum': 5000.0
                }
            ]
        }

        if os.path.exists('test_wallet.json'):
            with mock.patch(
                    'builtins.input',
                    side_effect=[
                        '2024-05-16', 'y', 'доход',
                        '5000', 'y', 'add_entry_test_description',
                        'y', 'y', ' '
                    ]):  # добавляем новую запись

                self.assertEqual(self.wallet.add_entry(), True)
                self.assertEqual(self.wallet.read_from_file(), result)

    def test_count_entries(self):

        self.create_test_file()

        self.assertEqual(self.wallet.count_entries(), 1)

    def test_edit_entries(self):

        self.create_test_file()

        result = {
            'balance': 500,
            'entries': [
                {
                    "id": 1,
                    "date": "2000-01-01 00:00:00.000001",
                    "operation": "доход",
                    "total_sum": 500,
                    "description": "test_description"
                }
            ]
        }

        if os.path.exists('test_wallet.json'):
            with mock.patch(
                    'builtins.input',
                    side_effect=[
                        '3', '1',
                        'y', '2', '2000-01-01',
                        'y', '', '0', '0'
                    ]):  # редактируем запись

                self.assertEqual(self.wallet.edit_entries(), None)
                self.assertEqual(self.wallet.read_from_file(), result)
