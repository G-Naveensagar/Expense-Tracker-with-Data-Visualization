from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("750x600")
        self.root.configure(bg="#f0f4f7")

        # --- Background Image ---
        try:
            self.bg_image = Image.open("background.jpg")  # Change to your image file name
            self.bg_image = self.bg_image.resize((750, 600), Image.ANTIALIAS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Background image not found or failed to load:", e)
        # -----------------------

        self.expenses = []
        self.file_path = "expenses.csv"
        self.load_expenses()

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#004c99", foreground="white")
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.map('Treeview', background=[('selected', '#add8e6')])
        
        title = tk.Label(self.root, text="Expense Tracker", font=("Helvetica", 20, "bold"), fg="#004c99", bg="#f0f4f7")
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#f0f4f7")
        frame.pack(pady=5)

        # Input Labels and Entries
        labels = ["Date (YYYY-MM-DD)", "Category", "Amount", "Description"]
        self.entries = []

        for i, text in enumerate(labels):
            tk.Label(frame, text=text, font=("Arial", 10), bg="#f0f4f7").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = tk.Entry(frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)

        tk.Button(frame, text="➕ Add Expense", font=("Arial", 10, "bold"), bg="#007acc", fg="white", command=self.add_expense).grid(row=4, column=0, columnspan=2, pady=10)

        # Button Panel
        btn_frame = tk.Frame(self.root, bg="#f0f4f7")
        btn_frame.pack(pady=10)

        buttons = [
            ("📋 View Expenses", self.view_expenses),
            ("📊 Visualize", self.visualize_expenses),
            ("🗓️ Monthly Summary", self.monthly_summary),
            ("💾 Save", self.save_expenses)
        ]
        for i, (text, cmd) in enumerate(buttons):
            tk.Button(btn_frame, text=text, font=("Arial", 10, "bold"), bg="#005b96", fg="white", width=18, command=cmd).grid(row=0, column=i, padx=5)

        # Expense Table
        self.tree = ttk.Treeview(self.root, columns=("Date", "Category", "Amount", "Description"), show='headings')
        for col in ("Date", "Category", "Amount", "Description"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(pady=10, fill="x", padx=20)

    def add_expense(self):
        date, category, amount, description = [e.get() for e in self.entries]

        try:
            amount = float(amount)
            self.expenses.append({
                "Date": date,
                "Category": category,
                "Amount": amount,
                "Description": description
            })
            self.tree.insert("", "end", values=(date, category, amount, description))
            for e in self.entries:
                e.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")

    def view_expenses(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for exp in self.expenses:
            self.tree.insert("", "end", values=(exp["Date"], exp["Category"], exp["Amount"], exp["Description"]))

    def save_expenses(self):
        df = pd.DataFrame(self.expenses)
        df.to_csv(self.file_path, index=False)
        messagebox.showinfo("Saved", f"Expenses saved to {self.file_path}")

    def load_expenses(self):
        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path)
            self.expenses = df.to_dict('records')

    def visualize_expenses(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "No expenses to visualize.")
            return
        df = pd.DataFrame(self.expenses)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')

        # Pie Chart
        category_totals = df.groupby('Category')['Amount'].sum()
        plt.figure(figsize=(8, 6))
        category_totals.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors)
        plt.title("Expense Distribution by Category")
        plt.ylabel("")
        plt.show()

        # Bar Chart
        monthly_totals = df.groupby('Month')['Amount'].sum()
        plt.figure(figsize=(10, 6))
        monthly_totals.plot(kind='bar', color='#60a3bc')
        plt.title("Monthly Expenses")
        plt.xlabel("Month")
        plt.ylabel("Total Amount")
        plt.tight_layout()
        plt.show()

    def monthly_summary(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "No expenses available.")
            return
        df = pd.DataFrame(self.expenses)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')
        summary = df.groupby('Month')['Amount'].sum()
        messagebox.showinfo("Monthly Summary", summary.to_string())

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

