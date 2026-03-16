"""
Parte 4 — Visualização Dinâmica em HTML
==================================================
Lê os três CSVs gerados na Parte 1 e cria um dashboard HTML único
com abas e tabelas roláveis contendo todos os países classificados.
"""

import pandas as pd
import os

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
HTML_PATH = os.path.join(RESULTS_DIR, "tabelas_medalhas.html")

def generate_table_html(df, table_id):
    """Gera o HTML para a tabela rolável do DataFrame com estilo."""
    # Renomeia colunas para visualização mais limpa se necessário
    html_table = df.to_html(classes="table_class", index=False, border=0, justify="center")
    
    # Adicionar o ID à tabela e um container div para a rolagem
    html_table = html_table.replace('<table class="table_class">', f'<table id="{table_id}" class="styled-table">')
    return f'<div class="table-container">\n{html_table}\n</div>'

print("Lendo resultados dos CSVs...")
df_verao = pd.read_csv(os.path.join(RESULTS_DIR, "medalhas_verao.csv"))
df_inverno = pd.read_csv(os.path.join(RESULTS_DIR, "medalhas_inverno.csv"))
df_total = pd.read_csv(os.path.join(RESULTS_DIR, "medalhas_total_geral.csv"))

print("Gerando HTML das tabelas...")
html_verao = generate_table_html(df_verao, "tabela_verao")
html_inverno = generate_table_html(df_inverno, "tabela_inverno")
html_total = generate_table_html(df_total, "tabela_total")

html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quadro de Medalhas — Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7f6;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }}
        .tabs {{
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }}
        .tab-button {{
            background-color: #fff;
            border: 2px solid #3498db;
            color: #3498db;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            margin: 0 5px;
            border-radius: 5px;
            transition: 0.3s;
        }}
        .tab-button:hover {{
            background-color: #ebf5fb;
        }}
        .tab-button.active {{
            background-color: #3498db;
            color: #fff;
        }}
        .tab-content {{
            display: none;
            max-width: 1000px;
            margin: 0 auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .tab-content.active {{
            display: block;
        }}
        .tab-content h2 {{
            color: #2c3e50;
            margin-top: 0;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        /* Estilos do container rolável */
        .table-container {{
            max-height: 600px;  /* Altura máxima da rolagem */
            overflow-y: auto;   /* Permite rolagem vertical */
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        /* Estilos da tabela */
        .styled-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 15px;
            text-align: center;
        }}
        .styled-table thead tr {{
            background-color: #2c3e50;
            color: #ffffff;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        .styled-table th, .styled-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #dddddd;
        }}
        /* Destaque para certas colunas */
        .styled-table th:nth-child(4), .styled-table td:nth-child(4) {{
            background-color: rgba(255, 215, 0, 0.1); /* Ouro suave */
            font-weight: bold;
        }}
        .styled-table th:nth-child(5), .styled-table td:nth-child(5) {{
            background-color: rgba(192, 192, 192, 0.1); /* Prata suave */
            font-weight: bold;
        }}
        .styled-table th:nth-child(6), .styled-table td:nth-child(6) {{
            background-color: rgba(205, 127, 50, 0.1); /* Bronze suave */
            font-weight: bold;
        }}
        .styled-table th:last-child, .styled-table td:last-child {{
            font-weight: bold;
            font-size: 16px;
            background-color: rgba(52, 152, 219, 0.1);
        }}
        .styled-table tbody tr:nth-of-type(even) {{
            background-color: #f9fbfd;
        }}
        .styled-table tbody tr:hover {{
            background-color: #f1f1f1;
        }}
        .styled-table tbody tr:first-of-type {{
            background-color: #fff9e6; /* Destaque leve para 1º lugar */
        }}
    </style>
</head>
<body>

    <h1>🏆 Quadro Histórico de Medalhas Olímpicas (1896-2024)</h1>

    <div class="tabs">
        <button class="tab-button active" onclick="openTab(event, 'verao')">☀️ Jogos de Verão</button>
        <button class="tab-button" onclick="openTab(event, 'inverno')">❄️ Jogos de Inverno</button>
        <button class="tab-button" onclick="openTab(event, 'total')">🌍 Total Geral</button>
    </div>

    <div id="verao" class="tab-content active">
        <h2>Medalhas — Jogos de Verão (159 Países)</h2>
        {html_verao}
    </div>

    <div id="inverno" class="tab-content">
        <h2>Medalhas — Jogos de Inverno (46 Países)</h2>
        {html_inverno}
    </div>

    <div id="total" class="tab-content">
        <h2>Medalhas — Total Geral (160 Países)</h2>
        {html_total}
    </div>

    <script>
        function openTab(evt, tabName) {{
            var i, tabcontent, tabbuttons;
            
            // Oculta todos os conteúdos
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {{
                tabcontent[i].classList.remove("active");
            }}
            
            // Remove a classe "active" dos botões
            tabbuttons = document.getElementsByClassName("tab-button");
            for (i = 0; i < tabbuttons.length; i++) {{
                tabbuttons[i].classList.remove("active");
            }}
            
            // Mostra o conteúdo atual e ativa o botão selecionado
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }}
    </script>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\\n✅ Concluído! HTML gerado em: {HTML_PATH}")
print("Abra o arquivo no seu navegador (ex: Chrome, Edge, Firefox) para visualizar as tabelas.")
