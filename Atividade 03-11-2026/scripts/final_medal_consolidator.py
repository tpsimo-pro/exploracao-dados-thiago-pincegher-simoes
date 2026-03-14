import json
import csv
import os

def consolidate_olympic_medals(input_json=os.path.join('data', 'processed', 'all_time_medals.json'), 
                               output_csv=os.path.join('results', 'reports', 'consolidated_medals_report.csv')):
    """
    Processes Olympic medal data from JSON into a consolidated CSV.
    The output includes Summer, Winter, and Overall totals per country.
    """
    
    # Check if input file exists
    if not os.path.exists(input_json):
        print(f"Error: Internal data file '{input_json}' not found.")
        print("Please ensure the Wikipedia extraction has been completed.")
        return

    try:
        with open(input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # Define headers for the output CSV
    headers = [
        'País',
        'Ouro (Verão)', 'Prata (Verão)', 'Bronze (Verão)', 'Total (Verão)',
        'Ouro (Inverno)', 'Prata (Inverno)', 'Bronze (Inverno)', 'Total (Inverno)',
        'Ouro (Total)', 'Prata (Total)', 'Bronze (Total)', 'Total Geral'
    ]

    try:
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for entry in data:
                # Extract country name and categorized medal counts
                country = entry.get('country', 'N/A')
                summer = entry.get('summer', {'gold': 0, 'silver': 0, 'bronze': 0, 'total': 0})
                winter = entry.get('winter', {'gold': 0, 'silver': 0, 'bronze': 0, 'total': 0})
                total = entry.get('total', {'gold': 0, 'silver': 0, 'bronze': 0, 'total': 0})
                
                row = [
                    country,
                    summer['gold'], summer['silver'], summer['bronze'], summer['total'],
                    winter['gold'], winter['silver'], winter['bronze'], winter['total'],
                    total['gold'], total['silver'], total['bronze'], total['total']
                ]
                writer.writerow(row)
        
        print(f"Successfully generated consolidated report: {output_csv}")
        
    except Exception as e:
        print(f"Error writing CSV file: {e}")

if __name__ == "__main__":
    consolidate_olympic_medals()
