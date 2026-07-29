from enum import StrEnum
from typing import Set

class Headers(StrEnum):
    """BudgetBaker CSV export headers mapped to internal names."""
    ACCOUNT         = "account"             # Name of the wallet/bank account (e.g., 'Cash', 'Revolut')
    CATEGORY        = "category"            # Transaction category (e.g., 'Groceries', 'Rent')
    CURRENCY        = "currency"            # Original currency of the transaction (e.g., 'EUR', 'USD')
    AMOUNT_RAW      = "amount"              # Value in the original currency
    AMOUNT          = "ref_currency_amount" # Value converted to your main reference currency
    DIRECTION       = "type"                # Direction of money: 'Uscita' (Expense) or 'Entrata' (Income)
    METHOD          = "payment_type"        # Method used (e.g., 'Cash', 'Debit Card', 'Bank Transfer')
    NOTE            = "note"                # Optional user description or memo
    TIMESTAMP       = "date"                # Timestamp in ISO 8601 format (UTC) 
    IS_TRANSFER     = "transfer"            # Boolean string ('true'/'false') indicating internal movements
    COUNTERPARTY    = "payee"               # The person or entity receiving/sending the money
    TAGS            = "labels"              # Tag strings used for custom filtering

    @classmethod
    def all(cls) -> Set[str]:
        """Return all field names as a set."""
        return {field.value for field in cls}

    @property
    def dtype(self) -> str:
        """Map each enum member to its corresponding Pandas dtype."""
        dtypes = {
            Headers.ACCOUNT: "string",
            Headers.CATEGORY: "string",
            Headers.CURRENCY: "string",
            Headers.AMOUNT_RAW: "float64",
            Headers.AMOUNT: "float64",
            Headers.DIRECTION: "string",
            Headers.METHOD: "string",
            Headers.NOTE: "string",
            Headers.TIMESTAMP: "datetime",
            Headers.IS_TRANSFER: "boolean",
            Headers.COUNTERPARTY: "string",
            Headers.TAGS: "string",
        }
        return dtypes[self]

    @property
    def target_name(self) -> str:
        """The clean, normalized column name to use in the DataFrame."""
        return self.name.lower()