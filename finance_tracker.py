import datetime
import json
import sqlite3
import logging
import tkinter as tk
from tkinter import messagebox

# Configure logging
logging.basicConfig(filename='finance.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class PersonalFinanceTracker:
    def __init__(self):
        self.transactions = []
        self.db_connection = sqlite3.connect("finance_data.db")
        self.cursor = self.db_connection.cursor()
        self.create_table()
        self.load_data()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                id INTEGER PRIMARY KEY,
                                date TEXT,
                                amount REAL,
                                category TEXT,
                                type TEXT)''')
        self.db_connection.commit()

    def add_transaction(self, amount, category, transaction_type):
        try:
            amount = float(amount)  # Ensure amount is a float
        except ValueError:
            raise ValueError("Invalid amount. Must be a number.")
        
        transaction = {
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "amount": amount,
            "category": category,
            "type": transaction_type
        }
        self.transactions.append(transaction)
        self.save_data()
        
        # Save to database
        self.cursor.execute("INSERT INTO transactions (date, amount, category, type) VALUES (?, ?, ?, ?)",
                            (transaction["date"], amount, category, transaction_type))
        self.db_connection.commit()
        
        # Logging
        logging.info(f"Added {transaction_type} - {category}: ${amount:.2f}")

    def generate_report(self):
        summary = {}
        for transaction in self.transactions:
            category = transaction["category"]
            amount = transaction["amount"]
            
            if category not in summary:
                summary[category] = 0
            summary[category] += amount if transaction["type"] == "income" else -amount
        
        print("\nMonthly Summary:")
        for category, total in summary.items():
            print(f"{category}: ${total:.2f}")
        
        # Save report to text file
        with open("finance_report.txt", "w") as file:
            for category, total in summary.items():
                file.write(f"{category}: ${total:.2f}\n")

    def save_data(self):
        with open("finance_data.json", "w") as file:
            json.dump(self.transactions, file, indent=4)

    def load_data(self):
        try:
            with open("finance_data.json", "r") as file:
                self.transactions = json.load(file)
        except FileNotFoundError:
            self.transactions = []

    def view_history(self):
        self.cursor.execute("SELECT * FROM transactions")
        records = self.cursor.fetchall()
        print("\nTransaction History:")
        for record in records:
            print(f"ID: {record[0]}, Date: {record[1]}, Amount: {record[2]}, Category: {record[3]}, Type: {record[4]}")

    def close(self):
        self.db_connection.close()

# Calculator for Arithmetic Operations
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

# GUI Implementation
class FinanceApp:
    def __init__(self, root, tracker):
        self.tracker = tracker
        self.root = root
        self.root.title("Personal Finance Tracker")
        
        tk.Label(root, text="Amount:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Category:").grid(row=1, column=0)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1)
        
        tk.Button(root, text="Add Income", command=self.add_income).grid(row=2, column=0)
        tk.Button(root, text="Add Expense", command=self.add_expense).grid(row=2, column=1)
        tk.Button(root, text="View Report", command=self.view_report).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="View History", command=self.view_history).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="Exit", command=self.exit_app).grid(row=5, column=0, columnspan=2)
    
    def add_income(self):
        self.add_transaction("income")
    
    def add_expense(self):
        self.add_transaction("expense")
    
    def add_transaction(self, transaction_type):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            if not category:
                raise ValueError("Category cannot be empty.")
            self.tracker.add_transaction(amount, category, transaction_type)
            messagebox.showinfo("Success", f"{transaction_type.capitalize()} added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid details.")
    
    def view_report(self):
        self.tracker.generate_report()
        messagebox.showinfo("Report", "Report generated and saved to finance_report.txt")
    
    def view_history(self):
        self.tracker.view_history()
    
    def exit_app(self):
        self.tracker.close()
        self.root.quit()

if __name__ == "__main__":
    tracker = PersonalFinanceTracker()
    mode = input("Choose mode: 1 for Console, 2 for GUI: ")
    if mode == "1":
        while True:
            print("\n1. Add Income\n2. Add Expense\n3. View Report\n4. View History\n5. Exit")
            choice = input("Choose an option: ")
            
            if choice == "1":
                amount = float(input("Enter income amount: "))
                category = input("Enter income category: ")
                tracker.add_transaction(amount, category, "income")
            elif choice == "2":
                amount = float(input("Enter expense amount: "))
                category = input("Enter expense category: ")
                tracker.add_transaction(amount, category, "expense")
            elif choice == "3":
                tracker.generate_report()
            elif choice == "4":
                tracker.view_history()
            elif choice == "5":
                tracker.close()
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please try again.")
    elif mode == "2":
        root = tk.Tk()
        app = FinanceApp(root, tracker)
        root.mainloop()
        tracker.close()
