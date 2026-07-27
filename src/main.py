from pathlib import Path
import csv

data_dir = Path(__file__).parent.parent / 'data'
filename = 'fake_wallet_record.csv'
data_file = data_dir / filename

with open(data_file, 'r', encoding='utf-8', newline='') as f:

    # DictReader: maps the information in each row to a dict
    # keys: values in the first row of file f will be used as the fieldnames
    reader = csv.DictReader(f, delimiter=';')

    for riga in reader:
        print(riga)