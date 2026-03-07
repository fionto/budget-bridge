from datetime import datetime

# Define the standard names I want to use inside my own system
# This allows me to switch data sources later without breaking my analysis code
INTERNAL_HEADERS = (
    'account',      # Name of the wallet/bank account (e.g., 'Cash', 'Revolut')
    'category',     # Transaction category (e.g., 'Groceries', 'Rent')
    'currency',     # Original currency of the transaction (e.g., 'EUR', 'USD')
    'amount_raw',   # Value in the original currency
    'amount',       # Value converted to your main reference currency
    'direction',    # Direction of money: 'Uscita' (Expense) or 'Entrata' (Income)
    'method',       # Method used (e.g., 'Cash', 'Debit Card', 'Bank Transfer')
    'note',         # Optional user description or memo
    'timestamp',    # Timestamp in ISO 8601 format (UTC)
    'is_transfer',  # Boolean string ('true'/'false') indicating internal movements
    'entity',       # The person or entity receiving/sending the money
    'tags'          # Tag strings used for custom filtering
)

def _safe_float(value_str: str) -> float:
    """
    Converts a string representation of a number to a float.

    This function handles whitespace stripping and catches conversion errors 
    gracefully to prevent pipeline crashes on dirty data.

    Args:
        value_str (str): The string value to convert (e.g., " 18.9 ", "").

    Returns:
        float: The converted floating-point number. If conversion fails 
            (e.g., empty string or non-numeric text), returns float('nan').
    """
    try:
        return float(value_str.strip())
    except ValueError:
        # I chose 'nan' instead of 0.0 because 'nan' propagates through math operations.
        return float("nan")

def _parse_date(date_str: str) -> datetime | None:
    """
    Parses an ISO 8601 date string into a datetime object.

    Handles specific formatting quirks from the source CSV, such as the 
    trailing 'Z' character for UTC time.

    Args:
        date_str (str): The date string in ISO 8601 format 
            (e.g., "2026-01-10T08:34:29.920Z").

    Returns:
        datetime | None: A Python datetime object if parsing is successful. 
            Returns None if the input is empty or the format is invalid.
    """
    try:
        # Removes the final 'Z' if present for compatibility with older versions of Python
        clean_date = date_str.replace('Z', '+00:00')
        return datetime.fromisoformat(clean_date)
    except ValueError:
        return None

dispatch_table = {
    'account'
}

def main():
    pass

if __name__ == "__main__":
    main()