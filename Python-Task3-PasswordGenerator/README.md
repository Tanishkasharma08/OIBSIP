# Random Password Generator — Advanced (Python Programming Track, Task 3)

## 📌 Objective
A GUI-based tool that generates strong, cryptographically secure passwords
based on user-defined criteria — length, character types, and ambiguous
character exclusion — with a live strength indicator and clipboard support.

## 🛠️ Tech Stack
- Python 3
- `secrets` — cryptographically secure random generation (not `random`)
- `tkinter` — GUI
- `pyperclip` — clipboard integration

## ✅ Features
- **GUI window** with a slider for password length (6–32 characters)
- **Checkboxes** to select character types: uppercase, lowercase, numbers, symbols
- Uses the **`secrets` module** (not `random`) for cryptographically secure generation
- **Security guarantee**: the generated password always contains at least one
  character from every selected type
- **Password strength indicator**: Weak / Medium / Strong, colour-coded, based
  on length and character diversity
- **"Copy to Clipboard"** button — copies the generated password instantly
  using `pyperclip`
- **Exclude ambiguous characters** option (removes `0`, `O`, `l`, `1`) via checkbox
- **Generation history** — the last 5 passwords generated in the current
  session are displayed (not saved to disk, for security)
- Input validation — warns if no character type is selected, and prompts for
  confirmation if the configuration would produce a weak password

## ▶️ How to Run
1. Install dependencies:
   ```bash
   pip install pyperclip
   ```
2. Run the app:
   ```bash
   python password_generator.py
   ```

## 🗂️ Project Structure
```
OIBSIP/Python-Task3-PasswordGenerator/
├── password_generator.py   # Main application
├── README.md                # This file
└── screenshots/              # App screenshots 
```

## 🧪 How It Works
1. Adjust the **length slider** to your desired password length.
2. Select which **character types** to include using the checkboxes.
3. Optionally check **"Exclude ambiguous characters"** to remove
   easily-confused characters like `0`, `O`, `l`, `1`.
4. Click **Generate Password** — the password appears along with its
   strength rating.
5. Click **Copy to Clipboard** to copy it instantly, ready to paste anywhere.
6. The last 5 generated passwords for this session are listed below for
   quick reference.

## 🔒 Security Notes
- The `secrets` module is used instead of `random` because it is designed
  for cryptographic purposes and is not predictable — making it suitable
  for generating passwords, tokens, and security-related values.
- Password history is kept **only in memory** for the current session and
  is never written to disk, to avoid leaving sensitive data behind.

## 👤 Author
Submitted as part of the **Oasis Infobyte Summer Internship Program (SIP)**
— Python Programming Track.
