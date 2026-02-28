# Define the exact headers provided by the BudgetBakers CSV export
# I'm using ALL_CAPS because these are constants that shouldn't change
BUDGETBAKERS_HEADERS = (
    "account", "category", "currency", "amount", "ref_currency_amount",
    "type", "payment_type", "note", "date", "transfer", "payee", "labels"
)

# Define the standard names I want to use inside my own system
# This allows me to switch data sources later without breaking my analysis code
INTERNAL_HEADERS = (
    'account', 'category', 'currency', 'amount_raw',
    'amount', 'direction', 'method', 'note',
    'timestamp', 'is_transfer', 'entity', 'tags'
)

def create_column_mapping(raw_headers: tuple[str], internal_headers: tuple[str]) -> dict:
    """Create a dictionary to map external CSV headers to internal standard names.

    This function ensures that the external data structure matches our expected 
    internal schema before creating the mapping. This prevents silent failures 
    during data processing.

    Args:
        raw_headers (tuple[str]): The column names exactly as they appear in the 
            source CSV file.
        internal_headers (tuple[str]): The standardized column names used within 
            the BudgetBridge system.

    Returns:
        dict: A mapping dictionary where keys are raw headers and values are 
            internal headers.

    Raises:
        ValueError: If the length of raw_headers does not match internal_headers.
            This indicates a configuration error in the column definitions.
    """
    # I'm checking lengths here to 'fail fast'. If I add a new column to one 
    # tuple but forget the other, I want to know immediately rather than getting 
    # weird data errors later.
    if len(raw_headers) != len(internal_headers):
        raise ValueError(
            f"Mapping mismatch! Raw: {len(raw_headers)} vs Internal: {len(internal_headers)}"
        )

    # I'm using a standard for-loop here instead of dict comprehension. 
    # I'm not fully comfortable with comprehensions yet, and this makes it 
    # easier for me to set breakpoints if I need to debug later.
    column_map = {}
    for raw_name, internal_name in zip(raw_headers, internal_headers):
        column_map[raw_name] = internal_name
    
    return column_map

def main():
    # Generate the mapping based on the defined constants
    header_map = create_column_mapping(BUDGETBAKERS_HEADERS, INTERNAL_HEADERS)
    print(header_map)

if __name__ == "__main__":
    main()