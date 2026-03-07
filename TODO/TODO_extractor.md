
# 📝 Developer Handoff: `extractor.py` Integration
**Date:** 28/02/2026
**Goal:** Merge individual logic modules into a single robust extraction script that outputs a `list[dict]`.

## ✅ Current Status (Completed & Tested)
Already written and tested these individual components:
1.  **Schema Validation:** `verify_header()` (Checks column count & names, raises `ValueError` on mismatch).
2.  **Row Parsing:** `parse_row()` (Splits strings, handles `_safe_float`, `_parse_date`, boolean conversion, returns `dict` or `None`).
3.  **File Iteration:** Basic `with open(...)` loop using `next()` to skip headers.
4.  **Constants:** `EXPECTED_HEADERS` and `INTERNAL_HEADERS` defined.

## 🚀 Tomorrow's Task List: The Merge

### Step 1: File Setup
- [✅] Create new file: `extractor.py`.
- [✅] Copy all imports (`datetime`) and Constants (`EXPECTED_HEADERS`, etc.) to the top.
- [ ] Copy helper functions: `_safe_float`, `_parse_date`.
- [ ] Copy main logic functions: `verify_header`, `parse_row`.
  - *Check:* Ensure docstrings are Google-style and inline "self-talk" comments are preserved.

### Step 2: Build the Orchestrator Function
[✅] Create a new function `run_extraction(file_path: str) -> list[dict]`:
- [✅] **Open File:** Use `with open(..., encoding='utf-8')`.
- [✅] **Header Check:**
  - Read the first line manually (`header_line = next(file)`).
  - Call `verify_header(header_line, EXPECTED_HEADERS)`.
  - *Logic:* If this raises an error, let it crash (Fail Fast) or catch it and print a clear message.
- [✅] **Process Rows:**
  - Iterate over the remaining lines (`for raw_line in file:`).
  - **Guard:** Skip empty lines (`if not raw_line.strip(): continue`).
  - **Parse:** Call `data = parse_row(raw_line)`.
  - **Collect:**
    - If `data` is valid: Append to `transactions` list.
    - If `data` is `None`: Increment an `error_count` variable (don't crash, just skip).
- [✅] **Return:** Return the final `transactions` list.

### Step 3: Main Execution Block
In `if __name__ == "__main__":`:
- [ ] Define the target file path (e.g., `"data/fake_wallet_record.csv"`).
- [ ] Wrap the call to `run_extraction` in a `try...except` block to catch `FileNotFoundError` or schema errors.
- [ ] **Reporting:** Print a summary:
  - "✅ Extraction Complete!"
  - "📊 Total Rows Processed: X"
  - "⚠️ Rows Skipped (Errors): Y"
- [ ] **Preview:** Print the first transaction dictionary to verify types (check that `amount` is float, `date` is datetime object).

## ⚠️ Critical Reminders & "Gotchas"
- **Encoding:** Keep `encoding='utf-8'` (or `utf-8-sig` if you see weird characters later).
- **Iterator Logic:** Remember, `next(file)` consumes the header. The `for` loop automatically starts at line 2. Do not try to read the header *inside* the loop.
- **Error Handling:**
  - `verify_header` should **raise** an error (stop everything if schema is wrong).
  - `parse_row` should **return None** for bad rows (skip one row, keep going).
- **Variable Names:** Ensure consistency (use English: `raw_line` instead of `riga`).
- **Mapping:** *Decision Point:* We currently map by position in `parse_row`. We have `INTERNAL_HEADERS` defined but aren't using them to rename keys yet.
  - *Option A:* Keep current logic (keys match source names).
  - *Option B:* Use the mapping dict to rename keys inside `parse_row` or after parsing.
  - *Recommendation for tomorrow:* Stick to Option A for now to get it working. Refactor to Option B in Phase 2 if needed.

## 🎯 Success Criteria
The script runs without crashing on the sample CSV, prints a success summary, and the first printed transaction shows:
- `amount` as a `float` (not string).
- `date` as a `datetime` object.
- `transfer` as a `bool`.