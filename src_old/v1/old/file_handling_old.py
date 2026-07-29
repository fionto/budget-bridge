# While testing with VSCode, my terminal is in budget-bridge/

with open('data/fake_wallet_record.csv', 'r', encoding='utf-8') as csv_source:
    
    header = csv_source.readline()
    raw_transactions = csv_source.readlines()

    for raw_transaction in raw_transactions:
        print(raw_transaction, end="")