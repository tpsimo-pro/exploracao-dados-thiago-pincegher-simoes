import json
import csv
import os

def consolidate_medals():
    input_file = os.path.join('data', 'processed', 'all_time_medals.json')
    results_dir = os.path.join('results', 'reports')
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Table 1: Medalhas – Jogos de Verão
    summer_sorted = sorted(data, key=lambda x: x['summer']['total'], reverse=True)
    save_csv(os.path.join(results_dir, 'medals_summer_sorted.csv'), summer_sorted, season='summer')

    # Table 2: Medalhas – Jogos de Inverno
    winter_sorted = sorted(data, key=lambda x: x['winter']['total'], reverse=True)
    save_csv(os.path.join(results_dir, 'medals_winter_sorted.csv'), winter_sorted, season='winter')

    # Table 3: Medalhas – Total Geral
    total_sorted = sorted(data, key=lambda x: x['total']['total'], reverse=True)
    save_csv(os.path.join(results_dir, 'medals_total_sorted.csv'), total_sorted, season='total')

def save_csv(filepath, data, season):
    if season == 'summer':
        headers = ['País', 'Ouro (Verão)', 'Prata (Verão)', 'Bronze (Verão)', 'Total (Verão)']
        rows = [[e['country'], e['summer']['gold'], e['summer']['silver'], e['summer']['bronze'], e['summer']['total']] for e in data]
    elif season == 'winter':
        headers = ['País', 'Ouro (Inverno)', 'Prata (Inverno)', 'Bronze (Inverno)', 'Total (Inverno)']
        rows = [[e['country'], e['winter']['gold'], e['winter']['silver'], e['winter']['bronze'], e['winter']['total']] for e in data]
    else:
        headers = ['País', 'Ouro (Total)', 'Prata (Total)', 'Bronze (Total)', 'Total Geral']
        rows = [[e['country'], e['total']['gold'], e['total']['silver'], e['total']['bronze'], e['total']['total']] for e in data]

    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Successfully saved {filepath}")

if __name__ == "__main__":
    consolidate_medals()
