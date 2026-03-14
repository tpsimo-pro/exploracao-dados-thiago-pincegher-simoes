import json
import os

def generate_dashboard():
    json_path = os.path.join('data', 'processed', 'all_time_medals.json')
    output_path = os.path.join('results', 'dashboard', 'dashboard.html')
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Sort data for the three categories (All countries)
    summer_all = sorted(data, key=lambda x: x['summer']['total'], reverse=True)
    winter_all = sorted(data, key=lambda x: x['winter']['total'], reverse=True)
    overall_all = sorted(data, key=lambda x: x['total']['total'], reverse=True)

    def generate_table_rows(items, season):
        rows = ""
        for i, item in enumerate(items):
            if season == 'summer':
                g, s, b, t = item['summer']['gold'], item['summer']['silver'], item['summer']['bronze'], item['summer']['total']
            elif season == 'winter':
                g, s, b, t = item['winter']['gold'], item['winter']['silver'], item['winter']['bronze'], item['winter']['total']
            else:
                g, s, b, t = item['total']['gold'], item['total']['silver'], item['total']['bronze'], item['total']['total']
            
            rows += f"""
                <tr>
                    <td>{i+1}</td>
                    <td class="country-name">{item['country']}</td>
                    <td class="gold">{g}</td>
                    <td class="silver">{s}</td>
                    <td class="bronze">{b}</td>
                    <td class="total-cell">{t}</td>
                </tr>
            """
        return rows

    html_content = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Medalhas Olímpicas</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-body: #0f172a;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.1);
            --accent-primary: #38bdf8;
            --gold: #fbbf24;
            --silver: #94a3b8;
            --bronze: #b45309;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }}

        body {{
            background-color: var(--bg-body);
            color: var(--text-main);
            padding: 2rem;
            min-height: 100vh;
            background-image: radial-gradient(circle at top right, #1e293b, #0f172a);
        }}

        header {{
            text-align: center;
            margin-bottom: 4rem;
        }}

        h1 {{
            font-weight: 800;
            font-size: 3rem;
            background: linear-gradient(to right, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}

        .subtitle {{
            color: var(--text-dim);
            font-size: 1.1rem;
        }}

        .dashboard-container {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 3rem;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .table-card {{
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 1.5rem;
            padding: 2rem;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }}

        .table-card:hover {{
            transform: translateY(-5px);
            border-color: rgba(56, 189, 248, 0.3);
        }}

        h2 {{
            margin-bottom: 1.5rem;
            font-weight: 600;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        h2::before {{
            content: '';
            display: block;
            width: 4px;
            height: 24px;
            background: var(--accent-primary);
            border-radius: 2px;
        }}

        .table-wrapper {{
            overflow-x: auto;
            max-height: 500px;
            overflow-y: auto;
            padding-right: 0.5rem;
        }}

        .table-wrapper::-webkit-scrollbar {{
            width: 6px;
        }}

        .table-wrapper::-webkit-scrollbar-track {{
            background: transparent;
        }}

        .table-wrapper::-webkit-scrollbar-thumb {{
            background: var(--glass-border);
            border-radius: 3px;
        }}

        .table-wrapper::-webkit-scrollbar-thumb:hover {{
            background: var(--accent-primary);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}

        th {{
            padding: 1rem;
            border-bottom: 1px solid var(--glass-border);
            color: var(--text-dim);
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            position: sticky;
            top: 0;
            background: #162035; /* Solid color for sticky header */
            z-index: 10;
        }}

        td {{
            padding: 1.25rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.02);
            font-size: 0.95rem;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}

        .country-name {{
            font-weight: 600;
            color: var(--text-main);
        }}

        .gold {{ color: var(--gold); font-weight: 600; }}
        .silver {{ color: var(--silver); font-weight: 600; }}
        .bronze {{ color: var(--bronze); font-weight: 600; }}
        .total-cell {{ font-weight: 800; color: var(--accent-primary); }}

        @media (max-width: 768px) {{
            body {{ padding: 1rem; }}
            h1 {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>

    <header>
        <h1>Quadro de Medalhas Olímpicas</h1>
        <p class="subtitle">Análise Consolidada de todos os tempos (Top 50 por Categoria)</p>
    </header>

    <div class="dashboard-container">
        
        <section class="table-card" id="verao">
            <h2>Jogos de Verão</h2>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Pos</th>
                            <th>País</th>
                            <th>Ouro</th>
                            <th>Prata</th>
                            <th>Bronze</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {generate_table_rows(summer_all, 'summer')}
                    </tbody>
                </table>
            </div>
        </section>

        <section class="table-card" id="inverno">
            <h2>Jogos de Inverno</h2>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Pos</th>
                            <th>País</th>
                            <th>Ouro</th>
                            <th>Prata</th>
                            <th>Bronze</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {generate_table_rows(winter_all, 'winter')}
                    </tbody>
                </table>
            </div>
        </section>

        <section class="table-card" id="geral">
            <h2>Total Geral</h2>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Pos</th>
                            <th>País</th>
                            <th>Ouro</th>
                            <th>Prata</th>
                            <th>Bronze</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {generate_table_rows(overall_all, 'total')}
                    </tbody>
                </table>
            </div>
        </section>

    </div>

</body>
</html>
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Dashboard gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    generate_dashboard()
