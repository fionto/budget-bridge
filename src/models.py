from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Transaction:
    # Mandatory fields (must come before fields with default values)
    account: str
    category: str
    currency: str
    amount_raw: float
    amount: float
    direction: str
    method: str
    timestamp: datetime
    
    # Optional fields (with default values)
    is_transfer: bool = False
    entity: Optional[str] = None
    note: Optional[str] = None
    tags: List[str] = field(default_factory=list)