from pathlib import Path

data_dir = Path(__file__).parent.parent / 'data'
filename = 'fake_wallet_record.csv'
data_file = data_dir / filename

with open(data_file, 'r', encoding='utf-8', newline='') as f:
    headings = f.readline().strip().split(';')

print(headings)