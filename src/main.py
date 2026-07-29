from pathlib import Path
import pandas as pd
from models import Headers
import utils

def main():
    """Execute the data processing from csv to dataframe."""

    # Targeting the file
    data_dir = Path(__file__).parent.parent / "data"
    filename = "fake_wallet_record.csv"
    data_file = data_dir / filename

    # Columns to read from CSV (uses the exact headers of the CSV export)
    usecols = Headers.original_headers()

    # Dtype mapping (excluding datetimes)
    dtype_schema = {
        header.value: header.dtype
        for header in Headers
        if header.dtype != "datetime64[ns]"
    }

    # Date columns to parse
    parse_dates = [
    header.value 
    for header in Headers
    if header.dtype == "datetime64[ns]"
    ]

    # Rename dictionary: CSV Header String -> Clean Internal Name
    rename_map = Headers.rename_map()

    # --- Read CSV ---
    df = pd.read_csv(
    data_file,
    sep=";",
    header=0,
    usecols=usecols,
    dtype=dtype_schema, # type: ignore
    parse_dates=parse_dates,
    )

    # --- Post-Processing ---
    # Rename CSV headers to clean member names ('ref_currency_amount' -> 'amount', etc.)
    df = df.rename(columns=rename_map)

    # Format Timestamp to Date only
    date_col = Headers.TIMESTAMP.target_name
    df[date_col] = df[date_col].dt.date

    # Round float columns in bulk
    float_cols = Headers.target_names_from_dtype("float64")
    df[float_cols] = df[float_cols].round(2)

    # Normalize string columns in bulk
    string_cols = Headers.target_names_from_dtype("string")
    for col in string_cols:
        # Replace empty strings with NA first
        df[col] = df[col].replace("", pd.NA)
        # Convert to object type and fill remaining NA with None
        df[col] = df[col].astype(object).where(df[col].notna(), None)

    # 5. Generate idempotency key for duplicates
    df['idempotency_key'] = df.apply(utils.generate_idempotency_key, axis=1)

    print(df.head())

if __name__ == "__main__":
    main()