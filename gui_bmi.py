import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime


# Initialize database
def init_db():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_data (
                      id INTEGER PRIMARY KEY,
                      date TEXT,
                      weight REAL,
                      height REAL,
                      bmi REAL)''')
    conn.commit()
    conn.close()


def save_bmi_data(date, weight, height, bmi):
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bmi_data (date, weight, height, bmi) VALUES (?, ?, ?, ?)", (date, weight, height, bmi))
    conn.commit()
    conn.close()


def fetch_bmi_data():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bmi_data")
    data = cursor.fetchall()
    conn.close()
    return data


# BMI Calculation
def calculate_bmi(weight, height):
    return weight / (height ** 2)


def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"


# GUI Application
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        # Weight input
        tk.Label(root, text="Weight (kg):").grid(row=0, column=0)
        self.weight_entry = tk.Entry(root)
        self.weight_entry.grid(row=0, column=1)

        # Height input
        tk.Label(root, text="Height (m):").grid(row=1, column=0)
        self.height_entry = tk.Entry(root)
        self.height_entry.grid(row=1, column=1)

        # Calculate button
        tk.Button(root, text="Calculate BMI", command=self.calculate_bmi).grid(row=2, column=0, columnspan=2)

        # Result
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=3, column=0, columnspan=2)

        # Historical Data button
        tk.Button(root, text="View Historical Data", command=self.view_historical_data).grid(row=4, column=0,
                                                                                             columnspan=2)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Weight and height must be positive values.")
                return

            bmi = calculate_bmi(weight, height)
            category = categorize_bmi(bmi)
            result_text = f"Your BMI is: {bmi:.2f}\nCategory: {category}"
            self.result_label.config(text=result_text)

            # Save data
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_bmi_data(date, weight, height, bmi)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for weight and height.")

    def view_historical_data(self):
        data = fetch_bmi_data()
        if not data:
            messagebox.showinfo("Info", "No historical data available.")
            return

        dates = [row[1] for row in data]
        bmis = [row[4] for row in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, bmis, marker='o')
        plt.xlabel('Date')
        plt.ylabel('BMI')
        plt.title('BMI Trend Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
