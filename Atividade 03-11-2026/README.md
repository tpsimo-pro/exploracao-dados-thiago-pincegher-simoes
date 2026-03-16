# Análise de Medalhas Olímpicas (1896–2024)

Projeto de exploração e análise dos dados históricos de medalhas dos Jogos Olímpicos, utilizando dois datasets complementares.

## 📂 Estrutura do Projeto

```text
k/
├── data_from_basedosdados/          # Dataset Olympedia (1896–2020)
│   ├── world_olympedia_olympics_game.csv.gz
│   ├── world_olympedia_olympics_game_medal_tally.csv.gz
│   └── world_olympedia_olympics_result.csv.gz
├── data_from_kaggle/                # Dataset Kaggle — Paris 2024
│   ├── medals_total.csv
│   ├── medals.csv
│   ├── medallists.csv
│   ├── nocs.csv
│   └── ...
├── results/
│   ├── medalhas_verao.csv           # Tabela consolidada — Jogos de Verão
│   ├── medalhas_inverno.csv         # Tabela consolidada — Jogos de Inverno
│   ├── medalhas_total_geral.csv     # Tabela consolidada — Total Geral
│   └── plots/
│       ├── top50_medalhas_verao.png
│       ├── top50_medalhas_inverno.png
│       └── top50_medalhas_total_geral.png
├── parte1_consolidacao_medalhas.py   # Parte 1 — Consolidação de medalhas
├── parte3_graficos_top50.py          # Parte 3 — Gráficos Top 50
└── README.md
```

## 🛠️ Pré-requisitos

- **Python 3.8+**
- Bibliotecas: `pandas`, `matplotlib`

Instalar dependências:
```powershell
pip install pandas matplotlib
```

## 🚀 Como Executar

### Parte 1 — Consolidação de Medalhas por País

Combina os dados do BaseDeDados (1896–2020) com os dados do Kaggle (Paris 2024), classificando cada edição como Verão ou Inverno, e gera três tabelas CSV ordenadas por total de medalhas.

```powershell
python parte1_consolidacao_medalhas.py
```

**Saída:**
- `results/medalhas_verao.csv` — 159 países
- `results/medalhas_inverno.csv` — 46 países
- `results/medalhas_total_geral.csv` — 160 países

O script também exibe no terminal:
- Top 10 de cada categoria
- Validações de integridade (Gold+Silver+Bronze = Total, Verão+Inverno = Total Geral)

---

### Parte 3 — Gráficos Top 50 Países

Gera três gráficos de barras horizontais empilhadas (Ouro, Prata, Bronze) com os países mais bem colocados em cada categoria.

```powershell
python parte3_graficos_top50.py
```

**Saída:**
- `results/plots/top50_medalhas_verao.png`
- `results/plots/top50_medalhas_inverno.png` (46 países — todos disponíveis)
- `results/plots/top50_medalhas_total_geral.png`

## ⚠️ Observação sobre os Dados

O dataset do BaseDeDados (fonte: Olympedia) **inclui os Jogos Intercalares de 1906** (Atenas), que **não são oficialmente reconhecidos pelo COI**. Isso causa pequenas diferenças nos totais em comparação com o [quadro oficial da Wikipedia](https://pt.wikipedia.org/wiki/Quadro_de_medalhas_dos_Jogos_Olímpicos), que exclui a edição de 1906.

---
*Projeto desenvolvido para a disciplina de Ciência de Dados.*
