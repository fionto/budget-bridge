from typing import Set

# Define the standard names I want to use inside my own system
# This allows me to switch data sources later without breaking my analysis code

class TransactionFieldNames:
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
        return {
            cls.ACCOUNT,
            cls.CATEGORY,
            cls.CURRENCY,
            cls.AMOUNT_RAW,
            cls.AMOUNT,
            cls.DIRECTION,
            cls.METHOD,
            cls.NOTE,
            cls.TIMESTAMP,
            cls.IS_TRANSFER,
            cls.ENTITY,
            cls.TAGS,
        }