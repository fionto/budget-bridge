# TODO: CSV_TO_INTERNAL_MAP (parallel to file_handling)

from datetime import datetime

# Number of fields in the header of the Wallet .csv as of 28/02/2026
EXPECTED_FIELDS_COUNT = 12

row_sample = (
    "Intesa Sanpaolo;Carburante;EUR;72.00;72.00;"
    "Uscita;Carta debito;;2025-12-21T13:05:33.120Z;"
    "false;Eni;Benzina"
)

def _safe_float(value_str: str) -> float:
    """
    Attempts to convert a string to float. 
    Returns float('nan') if conversion fails.
    """
    try:
        return float(value_str.strip())
    except ValueError:
        # This handles cases like empty strings or text in numeric fields
        return float("nan")

def _parse_date(date_str: str) -> datetime | None:
    try:
        # Removes the final 'Z' if present for compatibility with older versions of Python
        clean_date = date_str.replace('Z', '+00:00')
        return datetime.fromisoformat(clean_date)
    except ValueError:
        return None
    
def parse_row(row_str):
    """
    Parses a single CSV row into a structured dictionary.
    Returns None if the row is malformed to allow the caller to skip it.
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
        'trans_type': trans_type.upper(), # Normalizzazione
        'payment_type': payment_type,
        'notes': notes if notes else None, # Gestione campi vuoti
        'date': _parse_date(date_str),
        'transfer': transfer_str.lower() == 'true',
        'payee': payee,
        'labels': [l.strip() for l in labels.split(',')] if labels else [] # Trasforma in lista
    }

print(parse_row(row_sample))