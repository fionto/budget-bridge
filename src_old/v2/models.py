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
        """Return a human-readable, readable one-line summary."""
        # Format the date if present (e.g., "2026-07-27")
        date_str = self.timestamp.strftime("%Y-%m-%d") if self.timestamp else "No Date"
        
        # Build the directional arrow and amount string
        symbol = "-" if self.direction.upper() == "USCITA" else "+"
        amount_str = f"{symbol}{self.amount:.2f} {self.currency}"

        return f"[{date_str}] {amount_str:<12} | {self.account:<20} | {self.category}"

    @classmethod
    def from_dict(cls, row: dict) -> Transaction:
        """Create a Transaction instance from a row in the BudgetBakers CSV."""
        H = constants.OriginalHeaders

        # 1. Pulizia preventiva: rimuove spazi vuoti da TUTTE le stringhe della riga
        #    e converte le stringhe vuote in None in un solo colpo
        clean_row = {
            k: (v.strip() if isinstance(v, str) and v.strip() else None)
            for k, v in row.items()
        }

        # 2. Parsing dei tag (gestione sicura)
        raw_tags = clean_row.get(H.TAGS)
        tags_list = [t.strip() for t in raw_tags.split(",") if t.strip()] if raw_tags else []

        # 3. Assegnazione pulita e priva di ridondanze
        return cls(
            account     = row[H.ACCOUNT],
            category    = row[H.CATEGORY],
            currency    = row[H.CURRENCY],
            amount_raw  = utils._safe_float(clean_row.get(H.AMOUNT_RAW)),
            amount      = utils._safe_float(clean_row.get(H.AMOUNT)),
            direction   = (clean_row.get(H.DIRECTION) or "").upper(),
            timestamp   = utils._parse_date(clean_row.get(H.TIMESTAMP)),
            method      = clean_row.get(H.METHOD),
            is_transfer = str(clean_row.get(H.IS_TRANSFER, "")).lower() in ("true", "1", "yes"),
            entity      = clean_row.get(H.ENTITY),
            note        = clean_row.get(H.NOTE),
            tags        = tags_list,
        )