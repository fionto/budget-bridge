from pathlib import Path
import csv
from models import Transaction

data_dir = Path(__file__).parent.parent / 'data'
filename = 'fake_wallet_record.csv'
data_file = data_dir / filename

transactions = []

with open(data_file, 'r', encoding='utf-8', newline='') as f:

    # DictReader: maps the information in each row to a dict
    # keys: values in the first row of file f will be used as the fieldnames
    reader = csv.DictReader(f, delimiter=';')

    for row in reader:
        transaction = Transaction.from_dict(row)
        transactions.append(transaction)

for transaction in transactions:
    print(transaction.summary())