SOURCE_COLUMNS = (
    "account", "category", "currency", "amount", "ref_currency_amount",
    "type", "payment_type", "note", "date", "transfer", "payee", "labels"
)

MAPPED_COLUMNS = (
    'account', 'category', 'currency', 'amount_raw',
    'amount', 'direction', 'method', 'note',
    'timestamp', 'is_transfer', 'entity', 'tags'
)

def map_columns(source_columns: tuple[str], mapped_columns: tuple[str]) -> dict:
        # Validation: Fail fast if the developer made a typo
    if len(source_columns) != len(mapped_columns):
        # Raise an error to stop execution immediately
        raise ValueError(
            f"Mapping mismatch! Source: {len(source_columns)} vs Mapped: {len(mapped_columns)}"
        )

    # 3. Remapping
    header_mapping = {}
    for original, remapped in zip(source_columns, mapped_columns):
        header_mapping[original] = remapped
    
    return header_mapping

def main():
    mapped_dict = map_columns(SOURCE_COLUMNS, MAPPED_COLUMNS)
    print(mapped_dict)

main()