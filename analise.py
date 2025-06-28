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

#--------------ANALISE DE PREÇOS POR LABORATÓRIO-------------------
analise_laboratorio = df.groupby('Laboratorio')['PF Sem Impostos']
print("\n[ÀNALISE POR LABORATORIO] (Top 10 por Preço Medio)")
print(analise_laboratorio.head(10))
plt.figure(figsize=(12, 8))
analise_laboratorio.head(10)['mean'].sort_values().plot(kind='barh', color='skyblue')
plt.title('Preço Médio por Laboratório (PF Sem Impostos)')
plt.xlabel('Preço Médio (PF Sem Impostos)')
plt.ylabal('Laboratorio')
plt.show()

# Análise de Preço por Tipo de Produto
analise_tipo = df.groupby('TIPO DE PRODUTO (SEGREGAÇÃO)')['PF Sem Impostos'].describe()
print("\n--- Análise por Tipo de Produto ---")
print(analise_tipo)

# Visualização com Boxplot
plt.figure(figsize=(10, 7))
sns.boxplot(x='TIPO DE PRODUTO (SEGREGAÇÃO)', y='PF Sem Impostos', data=df)
plt.title('Distribuição de Preços por Tipo de Produto')
plt.ylabel('Preço (PF Sem Impostos)')
plt.xlabel('Tipo de Produto')

# Para visualizar 
plt.ylim(0, 200)
plt.show()

# Identificando outliers com o método IQR
Q1 = df['PF Sem Impostos'].quantile(0.25)
Q3 = df['PF Sem Impostos'].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 1.5 * IQR

outliers = df[df['PF Sem Impostos'] > limite_superior]

print(f"\n--- Análise de Outliers ---")
print(f"O limite superior para um preço ser considerado outlier é: R$ {limite_superior:.2f}")
print(f"Foram encontrados {len(outliers)} produtos considerados outliers.")
print("Exibindo os 10 mais caros entre eles:")
print(outliers.sort_values(by='PF Sem Impostos', ascending=False).head(10)[['PRODUTO', 'LABORATÓRIO', 'PF Sem Impostos']])

# os 20 mais comuns
top_20_apresentacoes = df['APRESENTAÇÃO'].value_counts().head(20)
print("\n--- Top 20 Apresentações Mais Comuns ---")
print(top_20_apresentacoes)

#preço medio de acordo com o laboratiorio
analise_competitiva = df.groupby('LABOATORIO')['PF Sem Impostos'].agg(['count', 'mean'])
analise_competitiva = analise_competitiva[analise_competitiva['count'] > 5 ]
#pra filtrar melho as parada
plt.figure(figsize=(12, 9))
sns.scatterplot(data=analise_competitiva, x='count', y='mean', s=100,alpha=0.7)

for i, row in analise_competitiva.head(10).iterrows():
    plt.text(row['count'], row['mean'], i, fontsize= 9)

plt.title('Matrix de Posicionamento Competitivo de Laboratórios')
plt.xlabel('Numero de Produtos(Volume de Portifolio)')
plt.ylabel('Preço Médio (Posicionamento de Valor)')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.show()

#--------------Caboooo-------------------
print("\nAnálise concluída.")

