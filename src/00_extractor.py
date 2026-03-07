from datetime import datetime
from pathlib import Path

# CONSTANTS
EXPECTED_HEADERS = (
    "account", "category", "currency", "amount", "ref_currency_amount",
    "type", "payment_type", "note", "date", "transfer", "payee", "labels"
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

def verify_header(raw_line: str, expected_headers: tuple[str, ...]) -> bool:
    """
    Verifies that the header line from a CSV file matches the expected internal schema.
    
    This function performs a strict check to ensure data integrity before processing.
    It fails fast by raising an error if the structure doesn't match exactly.

    Args:
        raw_line (str): The raw header string extracted from the CSV file.
        expected_headers (tuple[str]): The tuple of column names defined for the 
            internal BudgetBridge schema.

    Returns:
        bool: Returns True if validation passes successfully.

    Raises:
        ValueError: If the number of columns differs or if specific column names 
            do not match the expected schema.
    """
    
    # Clean the input: remove surrounding whitespace/newlines
    cleaned_line = raw_line.strip()
    
    # I'm converting to a tuple to match the type of 'expected_headers'.
    actual_columns = tuple(col.strip() for col in cleaned_line.split(';'))
    
    # Check 1: Verify the count of columns first.
    # This catches major structural issues quickly.
    if len(actual_columns) != len(expected_headers):
        raise ValueError(
            f"Column count mismatch -> Expected {len(expected_headers)}, found {len(actual_columns)}."
        )

    # Check 2: Verify each column name individually.
    # I use enumerate(zip(...)) here. 
    # Note: I cannot write 'for i, actual, expected' because zip() produces pairs (tuples).
    # enumerate() adds the index to those pairs, so I must unpack as: index, (item1, item2).
    for i, (actual, expected) in enumerate(zip(actual_columns, expected_headers)):
        if actual != expected:
            # Providing the index 'i' and the specific names makes debugging much faster.
            raise ValueError(
                f"Schema Mismatch at column index {i} -> Expected '{expected}', but found '{actual}'."
            )
    
    return True

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
    
    if len(fields) != len(EXPECTED_HEADERS):
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
        'amount_raw': _safe_float(amount_str),
        'amount': _safe_float(ref_amount_str),
        'direction': trans_type.upper(), # normalization
        'method': payment_type if payment_type else None, # managing empty field
        'note': notes if notes else None, # managing empty field
        'timestamp': _parse_date(date_str),
        'is_transfer': transfer_str.lower() == 'true',
        'entity': payee if payee else None, # managing empty field
        'tags': [l.strip() for l in labels.split(',')] if labels else [] # transform to list
    }

def run_extraction(file_path: Path) -> tuple[list[dict], int]:
    
    transactions = []
    error_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as csv_data:
        
        # TODO: How to verify if file is empty?      
        
        header_line = next(csv_data)
        verify_header(header_line, EXPECTED_HEADERS)

        for raw_line in csv_data:            
            raw_line = raw_line.strip()

            if not raw_line: 
                continue
            
            transaction = parse_row(raw_line)

            if transaction:
                transactions.append(transaction)
            else:
                error_count += 1

    return transactions, error_count


def main():

    fake_data_path = Path('data') / 'fake_wallet_record.csv'

    #TODO: i will perform file_exist check directly here

    transactions, errors = run_extraction(fake_data_path)

    print(transactions)

if __name__ == "__main__":
    main()