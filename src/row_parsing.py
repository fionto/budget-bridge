header = (
    "account;category;currency;amount;ref_currency_amount;"
    "type;payment_type;note;date;transfer;payee;labels"
)

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

def parse_row(row_str):
    
    transaction_fields = row_sample.strip().split(';')

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