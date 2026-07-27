# TODO: CSV_TO_INTERNAL_MAP
# TODO: EXPECTED_FIELDS_COUNT
# TODO: Early Exit / Guard Clauses
# TODO: Normalization (Case Insensitivity)

original_header = (
    "account;category;currency;amount;ref_currency_amount;"
    "type;payment_type;note;date;transfer;payee;labels"
)

# MAP here

from datetime import datetime

row_sample = (
    "Intesa Sanpaolo;Carburante;EUR;72.00;72.00;"
    "Uscita;Carta debito;;2025-12-21T13:05:33.120Z;"
    "false;Eni;Benzina"
)

def safe_float_convert(value_str: str) -> float:
    """
    Attempts to convert a string to float. 
    Returns float('nan') if conversion fails.
    """
    try:
        return float(value_str.strip())
    except ValueError:
        # This handles cases like empty strings or text in numeric fields
        return float("nan")
    
def check_transfer(transfer_str: str) -> bool | None:
    """
    Transform a 'true/false' string to float. 
    Returns None if conversion fails.
    """
    match transfer_str.strip().lower():
        case "true":
            return True
        case "false":
            return False
        case _:
            return None

def parse_row(row_str):
    """
    Parses a single CSV row into a structured dictionary.
    Returns None if the row is malformed to allow the caller to skip it.
    """    
    
    transaction_fields = row_str.strip().split(';')

    (
        account,              # Name of the wallet/bank account (e.g., 'Cash', 'Revolut')
        category,             # Transaction category (e.g., 'Groceries', 'Rent')
        currency,             # Original currency of the transaction (e.g., 'EUR', 'USD')
        amount,               # Value in the original currency
        ref_currency_amount,  # Value converted to your main reference currency
        trans_type,           # Direction of money: 'Uscita' (Expense) or 'Entrata' (Income)
        payment_type,         # Method used (e.g., 'Cash', 'Debit Card', 'Bank Transfer')
        notes,                # Optional user description or memo
        date,                 # Timestamp in ISO 8601 format (UTC)
        transfer,             # Boolean string ('true'/'false') indicating internal movements
        payee,                # The person or entity receiving/sending the money
        labels,               # Tag strings used for custom filtering
    ) = transaction_fields

    amount = safe_float_convert(amount)
    ref_currency_amount = safe_float_convert(ref_currency_amount)
    date = datetime.fromisoformat(date)
    transfer = check_transfer(transfer)

    parsed_data = {
        'account': account,
        'category': category,
        'currency': currency,
        'amount': amount,
        'ref_currency_amount': ref_currency_amount,
        'trans_type': trans_type,
        'payment_type': payment_type,
        'notes': notes,
        'date': date,
        'transfer': transfer,
        'payee': payee,
        'labels': labels
    }

    return parsed_data

print(parse_row(row_sample))