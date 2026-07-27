from enum import StrEnum
from typing import Set

class TransactionFieldNames(StrEnum):
    """Field names for the Transaction dataclass."""
    ACCOUNT     = 'account'     # Name of the wallet/bank account (e.g., 'Cash', 'Revolut')
    CATEGORY    = 'category'    # Transaction category (e.g., 'Groceries', 'Rent')
    CURRENCY    = 'currency'    # Original currency of the transaction (e.g., 'EUR', 'USD')
    AMOUNT_RAW  = 'amount_raw'  # Value in the original currency
    AMOUNT      = 'amount'      # Value converted to your main reference currency
    DIRECTION   = 'direction'   # Direction of money: 'Uscita' (Expense) or 'Entrata' (Income)
    METHOD      = 'method'      # Method used (e.g., 'Cash', 'Debit Card', 'Bank Transfer')
    NOTE        = 'note'        # Optional user description or memo
    TIMESTAMP   = 'timestamp'   # Timestamp in ISO 8601 format (UTC)
    IS_TRANSFER = 'is_transfer' # Boolean string ('true'/'false') indicating internal movements
    ENTITY      = 'entity'      # The person or entity receiving/sending the money
    TAGS        = 'tags'        # Tag strings used for custom filtering

    @classmethod
    def all(cls) -> Set[str]:
        """Return all metadata field names as a set."""
        # Generazione dinamica: zero manutenzione se aggiungi nuovi campi in futuro
        return {field.value for field in cls}


class OriginalHeaders(StrEnum):
    "Exact headers provided by the BudgetBakers CSV export"
    ACCOUNT     = "account"
    CATEGORY    = "category"
    CURRENCY    = "currency"
    AMOUNT_RAW  = "amount"
    AMOUNT      = "ref_currency_amount"
    DIRECTION   = "type"
    METHOD      = "payment_type"
    NOTE        = "note"
    TIMESTAMP   = "date"
    IS_TRANSFER = "transfer"
    ENTITY      = "payee"
    TAGS        = "labels"

    @classmethod
    def all(cls) -> Set[str]:
        """Return all metadata field names as a set."""
        # Generazione dinamica: zero manutenzione se aggiungi nuovi campi in futuro
        return {field.value for field in cls}