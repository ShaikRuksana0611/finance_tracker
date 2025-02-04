import unittest
import sqlite3
import os
from finance_tracker import PersonalFinanceTracker, Calculator

class TestFinanceTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = PersonalFinanceTracker()
        self.tracker.db_connection = sqlite3.connect(":memory:")  # Use in-memory DB for testing
        self.tracker.cursor = self.tracker.db_connection.cursor()
        self.tracker.create_table()
        self.tracker.transactions = []  # Reset transaction list

    def tearDown(self):
        self.tracker.db_connection.close()

    def test_add_transaction(self):
        self.tracker.add_transaction(100, "Salary", "income")
        self.assertEqual(len(self.tracker.transactions), 1)
        self.assertEqual(self.tracker.transactions[0]['amount'], 100)
        self.assertEqual(self.tracker.transactions[0]['category'], "Salary")
        self.assertEqual(self.tracker.transactions[0]['type'], "income")

    def test_generate_report(self):
        self.tracker.add_transaction(100, "Salary", "income")
        self.tracker.add_transaction(50, "Food", "expense")
        self.tracker.generate_report()
        with open("finance_report.txt", "r") as file:
            content = file.read()
        self.assertIn("Salary: $100.00", content)
        self.assertIn("Food: $-50.00", content)

    def test_view_history(self):
        self.tracker.add_transaction(100, "Salary", "income")
        self.tracker.add_transaction(50, "Food", "expense")
        self.tracker.cursor.execute("SELECT COUNT(*) FROM transactions")
        count = self.tracker.cursor.fetchone()[0]
        self.assertEqual(count, 2)

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Calculator.add(3, 2), 5)
    
    def test_subtract(self):
        self.assertEqual(Calculator.subtract(5, 3), 2)
    
    def test_multiply(self):
        self.assertEqual(Calculator.multiply(4, 3), 12)
    
    def test_divide(self):
        self.assertEqual(Calculator.divide(10, 2), 5)
        with self.assertRaises(ValueError):
            Calculator.divide(10, 0)

if __name__ == "__main__":
    unittest.main()