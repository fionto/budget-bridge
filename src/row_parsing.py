# TODO: CSV_TO_INTERNAL_MAP (parallel to file_handling)

from datetime import datetime

# # Constant: Expected number of columns based on the 
# Wallet CSV schema as of 28/02/2026
EXPECTED_FIELDS_COUNT = 12

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
    
def parse_row(row_str: str) -> dict | None:
    """
    Parses a single raw CSV row string into a structured dictionary.

    This function performs splitting, validation, and type conversion for all 
    12 expected fields. It acts as the primary cleaning step before data is 
    loaded into the Transaction model.

    Args:
        row_str (str): A single line from the CSV file containing semicolon-
            separated values.

    Returns:
        dict | None: A dictionary containing cleaned and typed data keys 
            (e.g., 'amount' as float, 'date' as datetime). Returns None if 
            the row is empty or has an incorrect number of columns.
    """
    if not row_str or not row_str.strip():
        return None
    
    fields = [f.strip() for f in row_str.split(';')]
    
    if len(fields) != EXPECTED_FIELDS_COUNT:
        return None

    (
        account,           # Name of the wallet/bank account (e.g., 'Cash', 'Revolut')
        category,          # Transaction category (e.g., 'Groceries', 'Rent')
        currency,          # Original currency of the transaction (e.g., 'EUR', 'USD')
        amount_str,        # Value in the original currency
        ref_amount_str,    # Value converted to your main reference currency
        trans_type,        # Direction of money: 'Uscita' (Expense) or 'Entrata' (Income)
        payment_type,      # Method used (e.g., 'Cash', 'Debit Card', 'Bank Transfer')
        notes,             # Optional user description or memo
        date_str,          # Timestamp in ISO 8601 format (UTC)
        transfer_str,      # Boolean string ('true'/'false') indicating internal movements
        payee,             # The person or entity receiving/sending the money
        labels,            # Tag strings used for custom filtering
    ) = fields

    return {
        'account': account,
        'category': category,
        'currency': currency,
        'amount': _safe_float(amount_str),
        'ref_currency_amount': _safe_float(ref_amount_str),
        'trans_type': trans_type.upper(), # normalization
        'payment_type': payment_type if payment_type else None, # managing empty field
        'notes': notes if notes else None, # managing empty field
        'date': _parse_date(date_str),
        'transfer': transfer_str.lower() == 'true',
        'payee': payee if payee else None, # managing empty field
        'labels': [l.strip() for l in labels.split(',')] if labels else [] # transform to list
    }

def main():
    row_sample = (
        "Intesa Sanpaolo;Carburante;EUR;72.00;72.00;"
        "Uscita;Carta debito;;2025-12-21T13:05:33.120Z;"
        "false;Eni;Benzina"
    )
    
    result = parse_row(row_sample)
    
    if result:
        print("✅ Parsing Successful:")
        print(f"Date Object: {result['date']} (Type: {type(result['date']).__name__})")
        print(f"Amount: {result['amount']} (Type: {type(result['amount']).__name__})")
        print(f"Is Transfer: {result['transfer']} (Type: {type(result['transfer']).__name__})")
        print(f"Labels: {result['labels']}")
    else:
        print("❌ Parsing Failed: Row was invalid.")

if __name__ == "__main__":
    main()