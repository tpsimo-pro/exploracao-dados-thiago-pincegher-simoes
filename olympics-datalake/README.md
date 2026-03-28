# 🏅 Olympics Data Lake — Paris 2024

Data Lake construído com dados dos Jogos Olímpicos de Paris 2024, organizado nas camadas **raw**, **bronze** e **gold**.

## Estrutura de Pastas

```
olympics-datalake/
├── README.md                    ← Este arquivo
├── metadata_schema.json         ← Schema técnico do Data Lake
│
├── raw/                         ← Dados brutos originais (CSV) + metadados JSON
│   ├── athletes.csv / .json
│   ├── coaches.csv / .json
│   ├── events.csv / .json
│   ├── medallists.csv / .json
│   ├── medals.csv / .json
│   ├── medals_total.csv / .json
│   ├── nocs.csv / .json
│   ├── schedules.csv / .json
│   ├── schedules_preliminary.csv / .json
│   ├── teams.csv / .json
│   ├── technical_officials.csv / .json
│   ├── torch_route.csv / .json
│   └── venues.csv / .json
│
├── bronze/                      ← Dados convertidos para Parquet + JOINs + metadados
│   ├── athletes.parquet / .json
│   ├── ... (demais arquivos convertidos)
│   ├── medallists_enriched.parquet / .json   ← JOIN medalistas + atletas + eventos
│   └── medals_by_country.parquet / .json     ← JOIN medalhas + NOCs
│
└── gold/                        ← Análises finais, visualizações, notebooks
    ├── analise_medalhas/
    │   ├── notebook.ipynb
    │   ├── medals_summary.csv
    │   ├── medals_plot.png
    │   └── metadata.json
    ├── analise_atletas/
    │   └── notebook.ipynb
    └── analise_genero/
        └── notebook.ipynb
```

## Fonte dos Dados

- **Origem:** Kaggle — [Paris 2024 Olympic Summer Games](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games)
- **Edição:** Jogos Olímpicos de Verão — Paris, França — 2024
- **Formato original:** CSV/XLSX exportado do dataset oficial

## Como Executar

1. Coloque os arquivos CSV na pasta `raw/`
2. Execute o notebook principal: `gold/analise_medalhas/notebook.ipynb`
3. Os arquivos Parquet serão gerados automaticamente em `bronze/`
4. As análises e visualizações serão salvas em `gold/`

## Dependências

```bash
pip install pandas pyarrow matplotlib seaborn jupyter
```
