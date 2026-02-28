# Simulating the first row of a .csv file (Normal Case)
RAW_HEADER_VALID = (
    "account;category;currency;amount;ref_currency_amount;"
    "type;payment_type;note;date;transfer;payee;labels"
)

# Simulating a broken header to test error handling (Error Case)
RAW_HEADER_INVALID = (
    "account;category;currency;sum;ref_currency_amount;"
    "type;payment_type;note;date;transfer;payee;labels"
)

# What I expect as of 28/02/2026 by downloading CSVs from Wallet
# Using ALL_CAPS to indicate these are constant configuration values
EXPECTED_HEADERS = (
    "account", "category", "currency", "amount", "ref_currency_amount",
    "type", "payment_type", "note", "date", "transfer", "payee", "labels"
)

def verify_header(raw_line: str, expected_headers: tuple[str]) -> bool:
    """
    Verifies that the header line from a CSV file matches the expected internal schema.
    
    This function performs a strict check to ensure data integrity before processing.
    It fails fast by raising an error if the structure doesn't match exactly.

    Args:
        raw_line (str): The raw header string extracted from the CSV file.
        expected_headers (tuple[str]): The tuple of column names defined for the 
            internal BudgetBridge schema.

    Returns:
        bool: Returns True if validation passes successfully.

    Raises:
        ValueError: If the number of columns differs or if specific column names 
            do not match the expected schema.
    """
    
    # Clean the input: remove surrounding whitespace/newlines
    cleaned_line = raw_line.strip()
    
    # I'm converting to a tuple to match the type of 'expected_headers'.
    actual_columns = tuple(col.strip() for col in cleaned_line.split(';'))
    
    # Check 1: Verify the count of columns first.
    # This catches major structural issues quickly.
    if len(actual_columns) != len(expected_headers):
        raise ValueError(
            f"Column count mismatch -> Expected {len(expected_headers)}, found {len(actual_columns)}."
        )

    # Check 2: Verify each column name individually.
    # I use enumerate(zip(...)) here. 
    # Note: I cannot write 'for i, actual, expected' because zip() produces pairs (tuples).
    # enumerate() adds the index to those pairs, so I must unpack as: index, (item1, item2).
    for i, (actual, expected) in enumerate(zip(actual_columns, expected_headers)):
        if actual != expected:
            # Providing the index 'i' and the specific names makes debugging much faster.
            raise ValueError(
                f"Schema Mismatch at column index {i} -> Expected '{expected}', but found '{actual}'."
            )
    
    return True

def main():
    """
    Runs elementary tests to verify the logic of verify_header().
    """
    print("--- Starting BudgetBridge Header Validation Tests ---\n")

    # Test 1: Valid Header
    print("Test 1: Validating correct header...")
    try:
        result = verify_header(RAW_HEADER_VALID, EXPECTED_HEADERS)
        if result:
            print("✅ PASS: Header validated successfully.\n")
    except ValueError as e:
        print(f"❌ FAIL: Unexpected error on valid data: {e}\n")

    # Test 2: Invalid Header (Simulating a typo in the source file)
    print("Test 2: Validating incorrect header (should fail)...")
    try:
        verify_header(RAW_HEADER_INVALID, EXPECTED_HEADERS)
    except ValueError as e:
        # We expect an error here, so catching it means the test passed.
        print("❌ FAIL:")
        print(f"   Error Message: {e}\n")

if __name__ == "__main__":
    main()