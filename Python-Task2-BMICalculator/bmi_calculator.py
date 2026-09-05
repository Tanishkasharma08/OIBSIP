"""
BMI Calculator — Advanced Tier
OASIS INFOBYTE — Python Programming Internship (Task 2)

Features:
- GUI built with tkinter (no command line)
- Input fields with labels for name, weight, and height + Calculate button
- Colour-coded result feedback based on BMI category
- Multi-user support: records saved per user name
- Historical records stored in an SQLite database
- Graph view: matplotlib line chart of a user's BMI trend over time
- Robust error handling for invalid input and database failures
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_FILE = "bmi_records.db"


# ---------------------------------------------------------------------------
# Database helper functions
# ---------------------------------------------------------------------------
def init_db():
    """Create the records table if it does not already exist."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date_recorded TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Could not initialise database:\n{e}")


def save_record(name, weight, height, bmi, category):
    """Insert a new BMI record into the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO records (name, weight, height, bmi, category, date_recorded)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, weight, height, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Could not save record:\n{e}")
        return False


def get_records_for_user(name):
    """Fetch all historical records for a given user, ordered by date."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT date_recorded, bmi, category, weight, height FROM records "
            "WHERE name = ? ORDER BY date_recorded ASC",
            (name,),
        )
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Could not fetch records:\n{e}")
        return []


def get_all_users():
    """Return a list of distinct user names present in the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT name FROM records ORDER BY name ASC")
        rows = [r[0] for r in cursor.fetchall()]
        conn.close()
        return rows
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Could not fetch users:\n{e}")
        return []


# ---------------------------------------------------------------------------
# BMI calculation logic
# ---------------------------------------------------------------------------
def calculate_bmi(weight, height):
    """Return BMI rounded to 2 decimal places."""
    bmi = weight / (height ** 2)
    return round(bmi, 2)


def classify_bmi(bmi):
    """Return (category, colour) tuple based on standard BMI thresholds."""
    if bmi < 18.5:
        return "Underweight", "#3498db"   # blue
    elif bmi < 25:
        return "Normal", "#27ae60"        # green
    elif bmi < 30:
        return "Overweight", "#f39c12"    # orange
    else:
        return "Obese", "#e74c3c"         # red


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator — Advanced")
        self.root.geometry("480x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f7")

        self._build_widgets()

    def _build_widgets(self):
        title_label = tk.Label(
            self.root, text="BMI Calculator", font=("Helvetica", 20, "bold"),
            bg="#f4f6f7", fg="#2c3e50"
        )
        title_label.pack(pady=(20, 10))

        form_frame = tk.Frame(self.root, bg="#f4f6f7")
        form_frame.pack(pady=10)

        # Name field
        tk.Label(form_frame, text="Name:", font=("Helvetica", 12), bg="#f4f6f7").grid(
            row=0, column=0, sticky="e", padx=10, pady=8
        )
        self.name_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=20)
        self.name_entry.grid(row=0, column=1, pady=8)

        # Weight field
        tk.Label(form_frame, text="Weight (kg):", font=("Helvetica", 12), bg="#f4f6f7").grid(
            row=1, column=0, sticky="e", padx=10, pady=8
        )
        self.weight_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=20)
        self.weight_entry.grid(row=1, column=1, pady=8)

        # Height field
        tk.Label(form_frame, text="Height (m):", font=("Helvetica", 12), bg="#f4f6f7").grid(
            row=2, column=0, sticky="e", padx=10, pady=8
        )
        self.height_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=20)
        self.height_entry.grid(row=2, column=1, pady=8)

        # Calculate button
        calc_btn = tk.Button(
            self.root, text="Calculate BMI", font=("Helvetica", 12, "bold"),
            bg="#2980b9", fg="white", relief="flat", padx=10, pady=6,
            command=self.on_calculate
        )
        calc_btn.pack(pady=15)

        # Result display
        self.result_frame = tk.Frame(self.root, bg="#f4f6f7")
        self.result_frame.pack(pady=5)

        self.result_label = tk.Label(
            self.result_frame, text="", font=("Helvetica", 16, "bold"), bg="#f4f6f7"
        )
        self.result_label.pack()

        self.category_label = tk.Label(
            self.result_frame, text="", font=("Helvetica", 14), bg="#f4f6f7"
        )
        self.category_label.pack()

        # Buttons: view graph
        graph_btn = tk.Button(
            self.root, text="📈 View BMI Trend Graph", font=("Helvetica", 11),
            bg="#8e44ad", fg="white", relief="flat", padx=8, pady=5,
            command=self.on_view_graph
        )
        graph_btn.pack(pady=(20, 5))

        info_label = tk.Label(
            self.root,
            text="Enter your name to save/view a personal BMI history.",
            font=("Helvetica", 9, "italic"), bg="#f4f6f7", fg="#7f8c8d"
        )
        info_label.pack(pady=(10, 0))

    # ------------------------------------------------------------------
    def on_calculate(self):
        name = self.name_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        height_str = self.height_entry.get().strip()

        # --- Input validation ---
        if not name:
            messagebox.showerror("Input Error", "Please enter your name.")
            return

        try:
            weight = float(weight_str)
            height = float(height_str)
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Weight and height must be numeric values.\n"
                "Example: weight = 65.5, height = 1.72"
            )
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Input Error",
                "Weight and height must be positive numbers greater than zero."
            )
            return

        # --- BMI calculation & classification ---
        bmi = calculate_bmi(weight, height)
        category, colour = classify_bmi(bmi)

        self.result_label.config(text=f"BMI: {bmi}", fg=colour)
        self.category_label.config(text=f"Category: {category}", fg=colour)

        # --- Save to database ---
        saved = save_record(name, weight, height, bmi, category)
        if saved:
            messagebox.showinfo("Saved", f"Record saved for {name}.")

    # ------------------------------------------------------------------
    def on_view_graph(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Enter a name first to view their trend graph.")
            return

        records = get_records_for_user(name)
        if not records:
            messagebox.showinfo("No Data", f"No historical records found for '{name}'.")
            return

        dates = [r[0][:10] for r in records]   # just the date portion
        bmis = [r[1] for r in records]

        graph_window = tk.Toplevel(self.root)
        graph_window.title(f"BMI Trend — {name}")
        graph_window.geometry("650x450")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dates, bmis, marker="o", color="#2980b9", linewidth=2)
        ax.set_title(f"BMI Trend for {name}")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.axhline(18.5, color="#3498db", linestyle="--", linewidth=0.8, label="Underweight/Normal")
        ax.axhline(25, color="#27ae60", linestyle="--", linewidth=0.8, label="Normal/Overweight")
        ax.axhline(30, color="#f39c12", linestyle="--", linewidth=0.8, label="Overweight/Obese")
        ax.legend(fontsize=8)
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()