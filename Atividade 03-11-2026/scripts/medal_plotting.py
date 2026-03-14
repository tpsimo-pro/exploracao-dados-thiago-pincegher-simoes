import pandas as pd
import matplotlib.pyplot as plt
import os

def create_charts():
    reports_dir = os.path.join('results', 'reports')
    files = {
        'summer': (os.path.join(reports_dir, 'medals_summer_sorted.csv'), 'Total (Verão)', 'Medalhas – Jogos de Verão'),
        'winter': (os.path.join(reports_dir, 'medals_winter_sorted.csv'), 'Total (Inverno)', 'Medalhas – Jogos de Inverno'),
        'total': (os.path.join(reports_dir, 'medals_total_sorted.csv'), 'Total Geral', 'Medalhas – Total Geral')
    }

    plt.style.use('ggplot')

    for key, (csv_file, column, title) in files.items():
        if not os.path.exists(csv_file):
            print(f"Warning: {csv_file} not found. Skipping...")
            continue
        
        df = pd.read_csv(csv_file)
        top_50 = df.head(50)

        plt.figure(figsize=(10, 8))
        # Horizontal bars for better readability of country names
        plt.barh(top_50['País'][::-1], top_50[column][::-1], color='skyblue')
        
        plt.xlabel('Total de Medalhas')
        plt.ylabel('País')
        plt.title(f'Top 50 Países: {title}')
        plt.tight_layout()
        
        print(f"Exibindo gráfico: {title} (Feche a janela para ver o próximo)")
        plt.show()

if __name__ == "__main__":
    create_charts()
