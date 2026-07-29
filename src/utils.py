import hashlib
import pandas as pd

def generate_idempotency_key(row) -> str:
    account = str(row["account"])
    date = str(row["timestamp"])
    category = str(row["category"])
    amount = str(row["amount"])
    note = "" if pd.isna(row["note"]) else str(row["note"])

    raw_str = f"{account}_{date}_{category}_{amount}_{note}"
    return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()