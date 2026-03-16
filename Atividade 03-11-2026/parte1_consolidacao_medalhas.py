"""
Parte 1 — Consolidação de Medalhas por País
============================================
Combina dados de dois datasets:
  - BaseDeDados (game_medal_tally.csv.gz): 1896–2020 (Verão + Inverno)
  - Kaggle (medals_total.csv): Paris 2024 (Verão)

Gera três CSVs consolidados com medalhas por país:
  - medalhas_verao.csv
  - medalhas_inverno.csv
  - medalhas_total_geral.csv
"""

import pandas as pd
import os

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASEDOSDADOS_DIR = os.path.join(BASE_DIR, "data_from_basedosdados")
KAGGLE_DIR = os.path.join(BASE_DIR, "data_from_kaggle")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Carregar dados do BaseDeDados (1896–2020)
# ---------------------------------------------------------------------------
print("=" * 60)
print("Carregando BaseDeDados (game_medal_tally)...")
df_tally = pd.read_csv(
    os.path.join(BASEDOSDADOS_DIR, "world_olympedia_olympics_game_medal_tally.csv.gz")
)

print(f"  Linhas: {len(df_tally)}")
print(f"  Colunas: {df_tally.columns.tolist()}")
print(f"  Edições únicas: {df_tally['edition'].nunique()}")

# Classificar Verão / Inverno a partir do nome da edição
# Nota: "1956 Equestrian" (evento equestre em Estocolmo) faz parte dos Jogos de Verão de 1956
# Nota: "1906 Intercalated" foram jogos intercalares de Verão em Atenas
def classify_season(edition):
    edition_str = str(edition)
    if "Summer" in edition_str:
        return "Summer"
    elif "Winter" in edition_str:
        return "Winter"
    elif "Equestrian" in edition_str or "Intercalated" in edition_str:
        return "Summer"  # Ambos são eventos de Verão
    else:
        return "Unknown"

df_tally["season"] = df_tally["edition"].apply(classify_season)

unknown = df_tally[df_tally["season"] == "Unknown"]
if len(unknown) > 0:
    print(f"  ⚠ {len(unknown)} linhas com season desconhecido:")
    print(unknown["edition"].unique())

print(f"  Verão: {df_tally[df_tally['season'] == 'Summer']['edition'].nunique()} edições")
print(f"  Inverno: {df_tally[df_tally['season'] == 'Winter']['edition'].nunique()} edições")

# ---------------------------------------------------------------------------
# 2. Verificar se Paris 2024 já existe; se não, adicionar do Kaggle
# ---------------------------------------------------------------------------
has_2024 = df_tally[df_tally["year"] == 2024]
if len(has_2024) == 0:
    print("\n  Paris 2024 NÃO encontrado no BaseDeDados. Adicionando do Kaggle...")
    df_2024 = pd.read_csv(os.path.join(KAGGLE_DIR, "medals_total.csv"))

    # Mapear colunas para o mesmo formato
    df_2024_mapped = pd.DataFrame({
        "year": 2024,
        "edition": "2024 Summer Olympics",
        "edition_id": -1,  # placeholder
        "country": df_2024["country"],
        "country_noc": df_2024["country_code"],
        "gold": df_2024["Gold Medal"],
        "silver": df_2024["Silver Medal"],
        "bronze": df_2024["Bronze Medal"],
        "total": df_2024["Total"],
        "season": "Summer",
    })

    df_tally = pd.concat([df_tally, df_2024_mapped], ignore_index=True)
    print(f"  ✔ Adicionados {len(df_2024_mapped)} registros de Paris 2024")
else:
    print(f"\n  Paris 2024 já presente ({len(has_2024)} registros).")

# ---------------------------------------------------------------------------
# 3. Verificar se Jogos de Inverno 2022 (Pequim) já existe; se não, avisar
# ---------------------------------------------------------------------------
has_2022 = df_tally[(df_tally["year"] == 2022) & (df_tally["season"] == "Winter")]
if len(has_2022) == 0:
    print("  ⚠ Inverno 2022 (Pequim) não encontrado nos dados.")
else:
    print(f"  ✔ Inverno 2022 presente ({len(has_2022)} registros).")

# ---------------------------------------------------------------------------
# 4. Agregação por País
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Agregando medalhas por país...")

def agregar_por_season(df, season_filter=None):
    """Agrega gold/silver/bronze/total por country_noc."""
    if season_filter:
        subset = df[df["season"] == season_filter].copy()
    else:
        subset = df.copy()

    agg = (
        subset.groupby("country_noc", as_index=False)
        .agg(
            gold=("gold", "sum"),
            silver=("silver", "sum"),
            bronze=("bronze", "sum"),
            total=("total", "sum"),
        )
    )

    # Buscar o nome mais recente do país para cada NOC
    nomes = (
        subset.sort_values("year", ascending=False)
        .drop_duplicates("country_noc", keep="first")[["country_noc", "country"]]
    )
    agg = agg.merge(nomes, on="country_noc", how="left")

    # Ordenar por total (desc), depois por ouro (desc)
    agg = agg.sort_values(["total", "gold"], ascending=[False, False]).reset_index(drop=True)
    agg.index += 1  # ranking começa em 1
    agg.index.name = "Rank"

    return agg

df_summer = agregar_por_season(df_tally, "Summer")
df_winter = agregar_por_season(df_tally, "Winter")
df_total = agregar_por_season(df_tally)

print(f"  Verão:  {len(df_summer)} países")
print(f"  Inverno: {len(df_winter)} países")
print(f"  Total:   {len(df_total)} países")

# ---------------------------------------------------------------------------
# 5. Exportar CSVs
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Exportando CSVs...")

def exportar_csv(df, filepath, label):
    """Salva DataFrame com cabeçalhos em português."""
    df_export = df.rename(columns={
        "country_noc": "NOC",
        "country": "País",
        "gold": "Ouro",
        "silver": "Prata",
        "bronze": "Bronze",
        "total": "Total",
    })[["NOC", "País", "Ouro", "Prata", "Bronze", "Total"]]

    df_export.to_csv(filepath, encoding="utf-8-sig")
    print(f"  ✔ {label}: {filepath}")

exportar_csv(df_summer, os.path.join(RESULTS_DIR, "medalhas_verao.csv"), "Jogos de Verão")
exportar_csv(df_winter, os.path.join(RESULTS_DIR, "medalhas_inverno.csv"), "Jogos de Inverno")
exportar_csv(df_total, os.path.join(RESULTS_DIR, "medalhas_total_geral.csv"), "Total Geral")

# ---------------------------------------------------------------------------
# 6. Exibir Top 10 de cada categoria
# ---------------------------------------------------------------------------
def mostrar_top(df, titulo, n=10):
    print(f"\n{'─' * 60}")
    print(f"  🏅 {titulo} — Top {n}")
    print(f"{'─' * 60}")
    display = df.head(n).rename(columns={
        "country_noc": "NOC",
        "country": "País",
        "gold": "Ouro",
        "silver": "Prata",
        "bronze": "Bronze",
        "total": "Total",
    })[["NOC", "País", "Ouro", "Prata", "Bronze", "Total"]]
    print(display.to_string())

print("\n" + "=" * 60)
print("RESULTADOS — Consolidação de Medalhas por País")
print("=" * 60)

mostrar_top(df_summer, "Jogos de Verão")
mostrar_top(df_winter, "Jogos de Inverno")
mostrar_top(df_total, "Total Geral (Verão + Inverno)")

# ---------------------------------------------------------------------------
# 7. Validações rápidas
# ---------------------------------------------------------------------------
print(f"\n{'=' * 60}")
print("VALIDAÇÕES")
print(f"{'=' * 60}")

# Verificar que gold + silver + bronze = total
for label, df_check in [("Verão", df_summer), ("Inverno", df_winter), ("Total", df_total)]:
    soma = df_check["gold"] + df_check["silver"] + df_check["bronze"]
    diff = (soma - df_check["total"]).abs().sum()
    status = "✔" if diff == 0 else "✘"
    print(f"  {status} {label}: Gold+Silver+Bronze = Total  (diff = {diff})")

# Verificar que soma de Verão + Inverno = Total Geral para cada NOC
merged = df_summer.rename(columns={"gold": "g_s", "silver": "s_s", "bronze": "b_s", "total": "t_s"})[["country_noc", "g_s", "s_s", "b_s", "t_s"]].merge(
    df_winter.rename(columns={"gold": "g_w", "silver": "s_w", "bronze": "b_w", "total": "t_w"})[["country_noc", "g_w", "s_w", "b_w", "t_w"]],
    on="country_noc", how="outer"
).fillna(0)

merged["soma_total"] = merged["t_s"] + merged["t_w"]
merged = merged.merge(
    df_total[["country_noc", "total"]], on="country_noc", how="left"
)
diff_total = (merged["soma_total"] - merged["total"]).abs().sum()
status = "✔" if diff_total == 0 else "✘"
print(f"  {status} Verão + Inverno = Total Geral  (diff = {diff_total})")

print(f"\n{'=' * 60}")
print("Concluído! Verifique os arquivos em: results/")
print(f"{'=' * 60}")
