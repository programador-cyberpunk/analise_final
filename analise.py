import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# configurando tudo os bagulho

# estilo seaborn, pra deixar tudo mais bonitinho
sns.set_style("whitegrid")

# carregando a leitura de dados
file_path = 'analise_final/preco_xarope_gov.csv'
try:
    df = pd.read_csv(analise_final/preco_xarope_gov.csv, sep=';', encoding='utf-8')
except FileNotFoundError:
    print(f"Deu bosta, aquivo '{analise_final/preco_xarope_gov.csv}' não encontrado.Verifique o caminho e tente de novo")
    exit()

#limpando a coluna de preço
df['PF Sem Impostos'] = df['PF Sem Impostos'].str.replace(',', '.').astype(float)
if 'PMC 0%' in df.columns:
    df['PMC 0%'] = df['PMC 0%'].str.replace(',', '.').astype(float)

#--------------ANALISE DESCRITIVA-------------------
print("Análise Descritiva:")
print("\n[INFO] visão geral dos dados: ")
df.info()

print("\n[ESTATISTICAS] resumo estatistico: 'PF Sem Impostos'")
print(df['PF Sem Impostos'].describe())

mode_price = df['PF Sem Impostos'].mode()[0]
print(f"\n[MODA] o preço de (PF Sem Impostos) eh: R${mode_price:.2f}")

#--------------ANALISE DE EXTREMOS-------------------
min_price = df['PF Sem Impostos'].min()
produto_min_price = df.loc[df['PF Sem Impostos'] == min_price]

print(f"\n[PREÇO MINIMO] O menor preço eh: R${min_price:.2f}")
print("Produto(s) com o menor preço: ")
print(produto_min_price[['Produto', 'Apresentação','PF Sem Impostos']])

max_price = df['PF Sem Impostos'].max()
produto_max_price = df.loc[df['PF Sem Impostos'] == max_price]

print(f"\n[PREÇO MAXIMO] O maior preço eh: R${max_price:.2f}")
print("Produto(s) com o maior preço: ")
print(produto_max_price[['Produto', 'Apresentação','PF Sem Impostos']])

#--------------CORRELAÇÂO-------------------
printf("\n Analise de correlação")
numeric_cols = df.select_dtypes(include=['float64', 'int64'])
correlation_matrix = numeric_cols.corr()

print("\n[MATRIZ DE CORELAÇÂO]")
print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Mapa da correlação entre variaveis')
plt.show()

#--------------ANALISE ADICIONAL-------------------
print("\n Analises adicionais: ")
print("\n Gerando o histograma pra visualiza a distribuição dos preços: ")

plt.figure(figsize=(10, 6))

sns.histplot(df[df['PF Sem Impostos'] < 100]['PF Sem Impostos'], bins=50, kde=True)
plt.title('Distribuição dos preços (PF Sem Impostos)')
plt.xlabel('Preço (PF Sem Impostos)')
plt.ylabel('Frequência')
plt.show()

print("\nAnálise concluída.")