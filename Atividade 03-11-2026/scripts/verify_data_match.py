import json
import csv
import os

def verify_data():
    json_path = os.path.join('data', 'processed', 'all_time_medals.json')
    csv_path = os.path.join('results', 'reports', 'consolidated_medals_report.csv')
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    # Load JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Load CSV
    csv_rows = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            csv_rows.append(row)

    if len(json_data) != len(csv_rows):
        print(f"Mismatch in count: JSON has {len(json_data)} entries, CSV has {len(csv_rows)}.")
        return

    errors = 0
    for i, entry in enumerate(json_data):
        csv_row = csv_rows[i]
        
        checks = [
            (entry['country'], csv_row['País']),
            (str(entry['summer']['gold']), csv_row['Ouro (Verão)']),
            (str(entry['summer']['silver']), csv_row['Prata (Verão)']),
            (str(entry['summer']['bronze']), csv_row['Bronze (Verão)']),
            (str(entry['summer']['total']), csv_row['Total (Verão)']),
            (str(entry['winter']['gold']), csv_row['Ouro (Inverno)']),
            (str(entry['winter']['silver']), csv_row['Prata (Inverno)']),
            (str(entry['winter']['bronze']), csv_row['Bronze (Inverno)']),
            (str(entry['winter']['total']), csv_row['Total (Inverno)']),
            (str(entry['total']['gold']), csv_row['Ouro (Total)']),
            (str(entry['total']['silver']), csv_row['Prata (Total)']),
            (str(entry['total']['bronze']), csv_row['Bronze (Total)']),
            (str(entry['total']['total']), csv_row['Total Geral'])
        ]
        
        for json_val, csv_val in checks:
            if json_val != csv_val:
                print(f"Mismatch at index {i} ({entry['country']}): Expected {json_val}, found {csv_val}")
                errors += 1

    if errors == 0:
        print("Success: All data in the CSV matches the source JSON perfectly.")
    else:
        print(f"Verification failed with {errors} mismatches.")

if __name__ == "__main__":
    verify_data()
