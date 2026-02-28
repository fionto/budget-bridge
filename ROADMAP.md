# 🛠️ Project Roadmap: Phase 1 - EXTRACTION

Goal: Successfully convert raw CSV data into a structured list of Python objects.

## 📂 File Handling & Environment
- [✅] Set up the project directory structure (`src/`, `data/`).
- [✅] Open and read a local `.csv` file using Python's built-in `open()` function.
- [✅] Handle the file header (skipping the first line of the CSV).

## 🧩 Row Parsing Logic
- [✅] Implement string splitting using the `;` delimiter.
- [✅] Clean "dirty" strings (removing extra whitespace with `.strip()`).
- [✅] **Data Normalization:**
    - [✅] Convert `amount` and `ref_currency_amount` from string to `float`.
    - [✅] Handle the `date` string (parsing the ISO 8601 format: `2026-02-10T...`).
    - [✅] Convert the `transfer` string (`"true"`/`"false"`) into actual Python Booleans.

## 🏗️ Transaction Class (The Data Model)
- [⚪] Define the `Transaction` class in `models.py`.
- [⚪] Implement `__init__` to map all 12 CSV columns:
    - `account`, `category`, `currency`, `amount`, `ref_currency_amount`, `type`, `payment_type`, `note`, `date`, `transfer`, `payee`, `labels`.
- [⚪] Create a `__repr__` or `__str__` method for easy debugging (printing the transaction).
- [⚪] Add a "Guard" method: `is_expense()` that returns `True` if type is 'Uscita' (or 'Expense').

## 🧪 Validation & Testing
- [⚪] Create a "dry run" script that parses 5 rows and prints them as objects.
- [⚪] Handle "Empty Cell" edge cases (e.g., when `note` or `labels` are missing).
- [⚪] Count total rows processed vs. total rows skipped due to errors.

---
*Status Key: ⚪ Not Started | 🔵 In Progress | ✅ Completed*