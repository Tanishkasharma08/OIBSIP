# BMI Calculator — Advanced (Python Programming Track, Task 2)

## 📌 Objective
A GUI-based Body Mass Index (BMI) calculator that classifies a user's BMI into
standard health categories, saves historical records per user in an SQLite
database, and visualises BMI trends over time using a line chart.

## 🛠️ Tech Stack
- Python 3
- `tkinter` — GUI
- `sqlite3` — data persistence
- `matplotlib` — trend visualisation

## ✅ Features
- GUI window with input fields for **Name**, **Weight (kg)**, and **Height (m)**
- **Calculate** button computes BMI using the formula `BMI = weight / height²`
- Result displayed with **colour-coded feedback**:
  - 🔵 Blue — Underweight (< 18.5)
  - 🟢 Green — Normal (18.5–24.9)
  - 🟠 Orange — Overweight (25–29.9)
  - 🔴 Red — Obese (≥ 30)
- **Multi-user support** — records are saved and retrieved by name
- **SQLite database** (`bmi_records.db`) stores every calculation with a timestamp
- **Graph view** — click "View BMI Trend Graph" to see a line chart of a user's
  BMI history over time, with reference lines for category boundaries
- **Input validation** — rejects empty names, non-numeric input, and
  zero/negative values with clear error messages
- **Error handling** — database read/write failures are caught and shown to
  the user instead of crashing the app

## ▶️ How to Run
1. Install dependencies:
   ```bash
   pip install matplotlib
   ```
2. Run the app:
   ```bash
   python bmi_calculator.py
   ```
3. The database file `bmi_records.db` is created automatically in the same
   folder on first run.

## 🗂️ Project Structure
```
OIBSIP/Python-Task2-BMICalculator/
├── bmi_calculator.py     # Main application
├── README.md             # This file
└── screenshots/          # App screenshots (add your own)
```

## 🧪 How It Works
1. Enter your name, weight, and height, then click **Calculate BMI**.
2. The app validates your input, computes BMI, and displays the category
   with a matching colour.
3. Every calculation is automatically saved to the database under your name.
4. Click **View BMI Trend Graph** (after entering your name) to see how your
   BMI has changed across multiple sessions.

## 👤 Author
Submitted as part of the **Oasis Infobyte Summer Internship Program (SIP)**
— Python Programming Track.
