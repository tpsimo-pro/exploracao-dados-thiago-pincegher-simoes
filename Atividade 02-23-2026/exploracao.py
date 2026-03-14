import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurar estilo dos gráficos
sns.set_theme(style="whitegrid")

# Caminhos
input_csv = r"c:\Users\Thiago-PC\Desktop\faculdade\cienciasDeDados\Atividade 23-02-2026\Planos De Ação Nacional Para A Conservação Das Espécies Ameaçadas De Extinção (PAN) - 2025 CSV_CLEANED.csv"
output_dir = r"c:\Users\Thiago-PC\Desktop\faculdade\cienciasDeDados\Atividade 23-02-2026\visualizacoes"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Carregando os dados...")
# Lendo o CSV limpo, o separador é ';' com base na inspeção anterior
df = pd.read_csv(input_csv, sep=";", encoding="utf-8-sig")

print("\n--- Informações Gerais e Tipos de Dados ---")
df.info()

print("\n--- Valores Ausentes por Coluna ---")
print(df.isnull().sum())

# Filtrar colunas numéricas (focar em panInicioAno e panFimAno)
# Converter para numérico, forçando erros para NaN para evitar problemas caso existam strings
df["panInicioAno"] = pd.to_numeric(df["panInicioAno"], errors="coerce")
df["panFimAno"] = pd.to_numeric(df["panFimAno"], errors="coerce")

num_cols = ["panInicioAno", "panFimAno"]

print("\n--- Estatísticas Descritivas ---")
for col in num_cols:
    print(f"\nEstatísticas para: {col}")
    data = df[col].dropna()
    if data.empty:
        print("Sem dados numéricos validos.")
        continue

    media = data.mean()
    mediana = data.median()
    moda = data.mode()
    minimo = data.min()
    maximo = data.max()
    desvio = data.std()
    variancia = data.var()
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1

    print(f"Média: {media:.2f}")
    print(f"Mediana: {mediana:.2f}")
    print(f"Moda: {moda.tolist()}")
    print(f"Mínimo: {minimo}")
    print(f"Máximo: {maximo}")
    print(f"Desvio Padrão: {desvio:.2f}")
    print(f"Variância: {variancia:.2f}")
    print(f"Q1 (25%): {q1:.2f}")
    print(f"Q3 (75%): {q3:.2f}")
    print(f"IQR: {iqr:.2f}")

print("\n--- Gerando Visualizações ---")

# 1. Histograma
plt.figure(figsize=(10, 6))
sns.histplot(
    data=df, x="panInicioAno", bins=15, kde=True, color="blue", label="Ano de Início"
)
sns.histplot(
    data=df, x="panFimAno", bins=15, kde=True, color="orange", label="Ano de Fim"
)
plt.title("Distribuição dos Anos de Início e Fim dos PANs")
plt.xlabel("Ano")
plt.ylabel("Frequência")
plt.legend()
plt.savefig(os.path.join(output_dir, "histograma_anos.png"))
plt.close()

# 2. Boxplot
plt.figure(figsize=(10, 6))
# Para o boxplot comparativo, derreter o DataFrame
df_melted = df.melt(
    value_vars=["panInicioAno", "panFimAno"], var_name="Tipo de Ano", value_name="Ano"
)
sns.boxplot(
    x="Tipo de Ano",
    y="Ano",
    data=df_melted,
    hue="Tipo de Ano",
    palette="Set2",
    legend=False,
)
plt.title("Boxplot: Dispersão dos Anos de Início e Fim")
plt.savefig(os.path.join(output_dir, "boxplot_anos.png"))
plt.close()

# 3. Gráfico de Dispersão (Scatter Plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="panInicioAno", y="panFimAno", alpha=0.7, color="green")
plt.title("Relação entre Ano de Início e Ano de Fim")
plt.xlabel("Ano de Início")
plt.ylabel("Ano de Fim")

# Adicionar linha de y=x para referência (projetos onde inicio=fim)
min_ano = min(df["panInicioAno"].min(), df["panFimAno"].min())
max_ano = max(df["panInicioAno"].max(), df["panFimAno"].max())
if pd.notna(min_ano) and pd.notna(max_ano):
    plt.plot([min_ano, max_ano], [min_ano, max_ano], "r--", label="Fim = Início")

plt.legend()
plt.savefig(os.path.join(output_dir, "scatter_anos.png"))
plt.close()

print(f"Gráficos salvos com sucesso no diretório: {output_dir}")
