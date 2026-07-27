from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import constants
import utils


@dataclass
class Transaction:
    # Mandatory fields (must come before fields with default values)
    account: str
    category: str
    currency: str
    amount_raw: float
    amount: float
    direction: str
    # Optional fields (with default values)
    timestamp: Optional[datetime]
    method: Optional[str] = None
    is_transfer: bool = False
    entity: Optional[str] = None
    note: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def summary(self) -> str:
        """Return a human-readable one-line summary."""
        return (f"Account {self.account} | {self.amount} €, {self.direction}")

    @classmethod
    def from_dict(cls, row: dict) -> Transaction:
        """
        Crea un'istanza di Transaction a partire da un dizionario (es. una riga di DictReader).
        Gestisce anche il parsing/casting dei tipi di dati.
        """
        # Convenient alias for readability
        H = constants.OriginalHeaders  # Alias comodo per leggibilità

        return cls(
            account     = row[H.ACCOUNT],
            category    = row[H.CATEGORY],
            currency    = row[H.CURRENCY],
            amount_raw  = utils._safe_float(row[H.AMOUNT_RAW]),
            amount      = utils._safe_float(row[H.AMOUNT]),
            direction   = row[H.DIRECTION].upper(),
            method      = row[H.METHOD] if row[H.METHOD] else None,
            timestamp   = utils._parse_date(row[H.TIMESTAMP]),
            is_transfer = row[H.IS_TRANSFER].lower() == 'true',
            entity      = row[H.ENTITY] if row[H.ENTITY] else None,
            tags        = [l.strip() for l in row[H.TAGS].split(',')] if row[H.TAGS] else [] # transform to list
        )