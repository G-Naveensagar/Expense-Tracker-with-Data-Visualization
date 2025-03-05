import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.file_path = "expenses.csv"
        self.load_expenses()

    def add_expense(self, date, category, amount, description):
        try:
            amount = float(amount)
            self.expenses.append({
                "Date": date,
                "Category": category,
                "Amount": amount,
                "Description": description
            })
            print("Expense added successfully!")
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses found.")
            return
        df = pd.DataFrame(self.expenses)
        print(df)

    def save_expenses(self):
        df = pd.DataFrame(self.expenses)
        df.to_csv(self.file_path, index=False)
        print(f"Expenses saved to {self.file_path}")

    def load_expenses(self):
        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path)
            self.expenses = df.to_dict('records')
            print(f"Expenses loaded from {self.file_path}")
        else:
            print("No existing expense file found. Starting fresh.")

    def visualize_expenses(self):
        if not self.expenses:
            print("No expenses to visualize.")
            return
        df = pd.DataFrame(self.expenses)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')

        # Pie Chart: Expense Distribution by Category
        category_totals = df.groupby('Category')['Amount'].sum()
        plt.figure(figsize=(8, 6))
        category_totals.plot(kind='pie', autopct='%1.1f%%', startangle=140)
        plt.title("Expense Distribution by Category")
        plt.ylabel("")
        plt.show()

        # Bar Chart: Monthly Expenses
        monthly_totals = df.groupby('Month')['Amount'].sum()
        plt.figure(figsize=(10, 6))
        monthly_totals.plot(kind='bar', color='skyblue')
        plt.title("Monthly Expenses")
        plt.xlabel("Month")
        plt.ylabel("Total Amount")
        plt.show()

    def monthly_summary(self):
        if not self.expenses:
            print("No expenses found.")
            return
        df = pd.DataFrame(self.expenses)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')
        monthly_totals = df.groupby('Month')['Amount'].sum()
        print("Monthly Summary:")
        print(monthly_totals)

def main():
    tracker = ExpenseTracker()
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Visualize Expenses")
        print("4. Monthly Summary")
        print("5. Save and Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            amount = input("Enter amount: ")
            description = input("Enter description: ")
            tracker.add_expense(date, category, amount, description)
        elif choice == "2":
            tracker.view_expenses()
        elif choice == "3":
            tracker.visualize_expenses()
        elif choice == "4":
            tracker.monthly_summary()
        elif choice == "5":
            tracker.save_expenses()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
