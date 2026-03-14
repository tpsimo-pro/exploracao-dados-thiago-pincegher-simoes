# Olympic Medal Analysis Project

Este projeto realiza a consolidação, análise e visualização dos dados históricos de medalhas dos Jogos Olímpicos (Verão, Inverno e Total Geral).

## 🚀 Como Funciona

O projeto segue um fluxo de dados estruturado:
1. **Extração**: Os dados atualizados foram extraídos do Wikipédia.
2. **Processamento**: Scripts Python limpam e consolidam os dados em arquivos CSV organizados por categorias e ordenados por total de medalhas.
3. **Visualização**: O projeto gera gráficos estatísticos (Matplotlib) e um Dashboard interativo (HTML/CSS) com design moderno.

## 📂 Estrutura de Pastas

A navegação pelos arquivos do projeto é organizada da seguinte forma:

```text
Atividade 03-11-2026/
├── data/
│   ├── raw/          # Bases de dados originais (CSV)
│   └── processed/    # Dados extraídos e convertidos (JSON)
├── scripts/          # Lógica de processamento e análise (Python)
├── results/
│   ├── dashboard/    # Dashboard interativo premium (HTML)
│   ├── plots/        # Gráficos estatísticos gerados (PNG)
│   └── reports/       # Tabelas consolidadas e ordenadas (CSV)
└── .venv/            # Ambiente virtual Python
```

## 🛠️ Scripts Principais

Localizados na pasta `scripts/`:

- `final_medal_consolidator.py`: Script principal para gerar o relatório consolidado final.
- `medal_consolidation.py`: Gera as tabelas CSV ordenadas por categoria.
- `dashboard_generator.py`: Gera o dashboard visual interativo.
- `medal_plotting.py`: Exibe gráficos de barras do Top 50 países.
- `verify_data_match.py`: Script de auditoria para garantir que o CSV condiz com o JSON original.

## 📈 Como Executar

1. **Ativar o Ambiente Virtual**:
   ```powershell
   .\.venv\Scripts\activate
   ```

2. **Gerar Relatórios e Dashboard**:
   ```powershell
   python scripts/medal_consolidation.py
   python scripts/dashboard_generator.py
   ```

3. **Ver o Dashboard**:
   Abra o arquivo `results/dashboard/dashboard.html` no seu navegador.

---
*Projeto desenvolvido para a disciplina de Ciência de Dados.*
