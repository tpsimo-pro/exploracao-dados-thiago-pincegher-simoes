"""
Parte 3 — Gráficos Top 50 Países por Medalhas
===============================================
Gera três gráficos de barras horizontais empilhadas (Ouro, Prata, Bronze)
para os 50 países mais bem colocados em cada categoria.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

TOP_N = 50

# Cores oficiais das medalhas
GOLD_COLOR = "#FFD700"
SILVER_COLOR = "#C0C0C0"
BRONZE_COLOR = "#CD7F32"

# Fonte
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 9,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor": "#FAFAFA",
    "axes.edgecolor": "#CCCCCC",
    "grid.color": "#E0E0E0",
    "grid.linestyle": "--",
    "grid.alpha": 0.7,
})


def create_medal_chart(csv_path, title, output_filename, top_n=TOP_N):
    """Cria gráfico de barras horizontais empilhadas para medalhas."""
    df = pd.read_csv(csv_path, index_col=0)
    df = df.head(top_n).copy()

    # Inverter para que o 1º lugar fique no topo
    df = df.iloc[::-1]

    # Labels: NOC + País (ex: "USA - United States")
    labels = [f"{row['NOC']} — {row['País']}" for _, row in df.iterrows()]

    fig, ax = plt.subplots(figsize=(14, max(12, top_n * 0.38)))

    y_pos = range(len(df))

    # Barras empilhadas
    bars_gold = ax.barh(y_pos, df["Ouro"], color=GOLD_COLOR, edgecolor="white",
                        linewidth=0.5, label="Ouro", height=0.7)
    bars_silver = ax.barh(y_pos, df["Prata"], left=df["Ouro"], color=SILVER_COLOR,
                          edgecolor="white", linewidth=0.5, label="Prata", height=0.7)
    bars_bronze = ax.barh(y_pos, df["Bronze"], left=df["Ouro"] + df["Prata"],
                          color=BRONZE_COLOR, edgecolor="white", linewidth=0.5,
                          label="Bronze", height=0.7)

    # Total no final de cada barra
    for i, (_, row) in enumerate(df.iterrows()):
        total = row["Total"]
        ax.text(total + (df["Total"].max() * 0.008), i, f" {int(total)}",
                va="center", ha="left", fontsize=7, fontweight="bold", color="#333333")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("Número de Medalhas", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_title(title, fontsize=16, fontweight="bold", pad=15, color="#1a1a2e")

    # Ajustar limites do eixo x para caber o texto do total
    ax.set_xlim(0, df["Total"].max() * 1.08)

    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=10))
    ax.grid(axis="x", alpha=0.5)
    ax.legend(loc="lower right", fontsize=10, frameon=True, fancybox=True,
              shadow=True, framealpha=0.9)

    # Rank numérico à esquerda
    ax.tick_params(axis="y", which="both", length=0)
    ax.invert_yaxis()  # Já invertemos o df, então re-inverter o eixo para manter 1º no topo

    # Na verdade, como invertemos o df, o 1º lugar está na última posição (bottom).
    # invert_yaxis coloca o bottom no topo. Perfeito.

    plt.tight_layout()

    output_path = os.path.join(PLOTS_DIR, output_filename)
    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✔ Salvo: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# Gerar os 3 gráficos
# ---------------------------------------------------------------------------
print("=" * 60)
print("Gerando gráficos Top 50 por categoria...")
print("=" * 60)

charts = [
    {
        "csv": os.path.join(RESULTS_DIR, "medalhas_verao.csv"),
        "title": "Top 50 Países — Medalhas nos Jogos de Verão",
        "filename": "top50_medalhas_verao.png",
    },
    {
        "csv": os.path.join(RESULTS_DIR, "medalhas_inverno.csv"),
        "title": "Top 50 Países — Medalhas nos Jogos de Inverno",
        "filename": "top50_medalhas_inverno.png",
    },
    {
        "csv": os.path.join(RESULTS_DIR, "medalhas_total_geral.csv"),
        "title": "Top 50 Países — Medalhas Total Geral",
        "filename": "top50_medalhas_total_geral.png",
    },
]

for chart in charts:
    # Para inverno, limitar ao nº de países disponíveis (46)
    df_check = pd.read_csv(chart["csv"], index_col=0)
    actual_top = min(TOP_N, len(df_check))
    if actual_top < TOP_N:
        print(f"\n  ℹ {chart['filename']}: apenas {actual_top} países disponíveis.")
        chart["title"] = chart["title"].replace("Top 50", f"Top {actual_top}")

    create_medal_chart(chart["csv"], chart["title"], chart["filename"], top_n=actual_top)

print(f"\n{'=' * 60}")
print(f"Concluído! Gráficos salvos em: {PLOTS_DIR}")
print(f"{'=' * 60}")
