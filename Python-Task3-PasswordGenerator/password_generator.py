"""
Random Password Generator — Advanced Tier
OASIS INFOBYTE — Python Programming Internship (Task 3)

Features:
- GUI window with slider for length control and checkboxes for character types
- Uses the `secrets` module (cryptographically secure) instead of `random`
- Password strength indicator (Weak / Medium / Strong)
- Security rule enforced: guaranteed at least one character from each selected type
- "Copy to Clipboard" button using pyperclip
- Option to exclude ambiguous characters (0, O, l, 1)
- Generation history: last 5 passwords shown in the session (not persisted to file)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


AMBIGUOUS_CHARS = "0Ol1"


# ---------------------------------------------------------------------------
# Password generation logic
# ---------------------------------------------------------------------------
def build_character_pool(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    """Build the pool of characters to sample from, based on selected options."""
    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += "!@#$%^&*()-_=+[]{};:,.<>?"

    if exclude_ambiguous:
        pool = "".join(ch for ch in pool if ch not in AMBIGUOUS_CHARS)

    return pool


def generate_secure_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    """
    Generate a cryptographically secure password that is guaranteed to
    contain at least one character from each selected character type.
    """
    selected_types = []
    if use_upper:
        selected_types.append(string.ascii_uppercase)
    if use_lower:
        selected_types.append(string.ascii_lowercase)
    if use_digits:
        selected_types.append(string.digits)
    if use_symbols:
        selected_types.append("!@#$%^&*()-_=+[]{};:,.<>?")

    if exclude_ambiguous:
        selected_types = [
            "".join(ch for ch in group if ch not in AMBIGUOUS_CHARS)
            for group in selected_types
        ]

    pool = build_character_pool(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous)

    if not pool:
        raise ValueError("No character type selected.")
    if length < len(selected_types):
        raise ValueError("Password length is too short for the selected character types.")

    # Guarantee at least one character from each selected type
    password_chars = [secrets.choice(group) for group in selected_types if group]

    # Fill the rest of the password length randomly from the full pool
    remaining = length - len(password_chars)
    password_chars += [secrets.choice(pool) for _ in range(remaining)]

    # Shuffle securely so the guaranteed characters aren't always at the start
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


def evaluate_strength(password, type_count):
    """
    Return (label, colour) describing password strength based on
    length and character diversity.
    """
    length = len(password)

    if length < 8 or type_count <= 1:
        return "Weak", "#e74c3c"       # red
    elif length < 12 or type_count == 2:
        return "Medium", "#f39c12"     # orange
    else:
        return "Strong", "#27ae60"     # green


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------
class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator — Advanced")
        self.root.geometry("480x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f7")

        self.history = []  # session-only history, max 5 items

        self._build_widgets()

    def _build_widgets(self):
        tk.Label(
            self.root, text="🔐 Password Generator", font=("Helvetica", 20, "bold"),
            bg="#f4f6f7", fg="#2c3e50"
        ).pack(pady=(20, 10))

        # --- Length slider ---
        length_frame = tk.Frame(self.root, bg="#f4f6f7")
        length_frame.pack(pady=10, fill="x", padx=30)

        tk.Label(length_frame, text="Password Length:", font=("Helvetica", 12), bg="#f4f6f7").pack(anchor="w")

        self.length_var = tk.IntVar(value=12)
        self.length_display = tk.Label(
            length_frame, text="12", font=("Helvetica", 12, "bold"), bg="#f4f6f7", fg="#2980b9"
        )
        self.length_display.pack(anchor="e")

        self.length_slider = tk.Scale(
            length_frame, from_=6, to=32, orient="horizontal",
            variable=self.length_var, showvalue=False,
            command=self._on_length_change, bg="#f4f6f7", troughcolor="#dfe6e9"
        )
        self.length_slider.pack(fill="x")

        # --- Character type checkboxes ---
        options_frame = tk.LabelFrame(
            self.root, text="Character Types", font=("Helvetica", 11, "bold"),
            bg="#f4f6f7", padx=15, pady=10
        )
        options_frame.pack(pady=15, fill="x", padx=30)

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        tk.Checkbutton(options_frame, text="Uppercase Letters (A-Z)", variable=self.use_upper,
                        bg="#f4f6f7", font=("Helvetica", 10)).pack(anchor="w")
        tk.Checkbutton(options_frame, text="Lowercase Letters (a-z)", variable=self.use_lower,
                        bg="#f4f6f7", font=("Helvetica", 10)).pack(anchor="w")
        tk.Checkbutton(options_frame, text="Numbers (0-9)", variable=self.use_digits,
                        bg="#f4f6f7", font=("Helvetica", 10)).pack(anchor="w")
        tk.Checkbutton(options_frame, text="Symbols (!@#$%^&*)", variable=self.use_symbols,
                        bg="#f4f6f7", font=("Helvetica", 10)).pack(anchor="w")
        tk.Checkbutton(options_frame, text="Exclude ambiguous characters (0, O, l, 1)",
                        variable=self.exclude_ambiguous, bg="#f4f6f7", font=("Helvetica", 10)).pack(anchor="w")

        # --- Generate button ---
        tk.Button(
            self.root, text="Generate Password", font=("Helvetica", 12, "bold"),
            bg="#2980b9", fg="white", relief="flat", padx=10, pady=8,
            command=self.on_generate
        ).pack(pady=15)

        # --- Result display ---
        result_frame = tk.Frame(self.root, bg="#f4f6f7")
        result_frame.pack(pady=5, fill="x", padx=30)

        self.password_display = tk.Entry(
            result_frame, font=("Consolas", 14), justify="center", state="readonly"
        )
        self.password_display.pack(fill="x", pady=5)

        self.strength_label = tk.Label(
            result_frame, text="", font=("Helvetica", 12, "bold"), bg="#f4f6f7"
        )
        self.strength_label.pack(pady=(5, 0))

        tk.Button(
            self.root, text="📋 Copy to Clipboard", font=("Helvetica", 11),
            bg="#8e44ad", fg="white", relief="flat", padx=8, pady=5,
            command=self.on_copy
        ).pack(pady=10)

        # --- History ---
        history_frame = tk.LabelFrame(
            self.root, text="Last 5 Generated Passwords (this session)",
            font=("Helvetica", 10, "bold"), bg="#f4f6f7", padx=10, pady=10
        )
        history_frame.pack(pady=10, fill="both", padx=30, expand=True)

        self.history_listbox = tk.Listbox(history_frame, font=("Consolas", 10), height=6)
        self.history_listbox.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    def _on_length_change(self, value):
        self.length_display.config(text=str(value))

    def on_generate(self):
        length = self.length_var.get()
        use_upper = self.use_upper.get()
        use_lower = self.use_lower.get()
        use_digits = self.use_digits.get()
        use_symbols = self.use_symbols.get()
        exclude_ambiguous = self.exclude_ambiguous.get()

        type_count = sum([use_upper, use_lower, use_digits, use_symbols])

        # --- Validation ---
        if type_count == 0:
            messagebox.showerror("Selection Error", "Please select at least one character type.")
            return

        if type_count < 2:
            proceed = messagebox.askyesno(
                "Weak Configuration",
                "Only one character type is selected. This will produce a weak password.\n"
                "Do you want to continue anyway?"
            )
            if not proceed:
                return

        try:
            password = generate_secure_password(
                length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous
            )
        except ValueError as e:
            messagebox.showerror("Generation Error", str(e))
            return

        # --- Display result ---
        self.password_display.config(state="normal")
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, password)
        self.password_display.config(state="readonly")

        strength_label, colour = evaluate_strength(password, type_count)
        self.strength_label.config(text=f"Strength: {strength_label}", fg=colour)

        # --- Update history (max 5, most recent on top) ---
        self.history.insert(0, password)
        self.history = self.history[:5]
        self.history_listbox.delete(0, tk.END)
        for pw in self.history:
            self.history_listbox.insert(tk.END, pw)

    def on_copy(self):
        password = self.password_display.get()
        if not password:
            messagebox.showwarning("Nothing to Copy", "Generate a password first.")
            return

        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Copied", "Password copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Clipboard Error", f"Could not copy to clipboard:\n{e}")
        else:
            messagebox.showwarning(
                "pyperclip Not Installed",
                "Install pyperclip to enable clipboard copying:\npip install pyperclip"
            )


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()