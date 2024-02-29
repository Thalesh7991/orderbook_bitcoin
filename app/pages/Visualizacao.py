import sys
sys.path.append('../')  
import pandas as pd
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from src.data.collector.brasil_bitcoin import LoadBrasilBitcoin
from src.data.collector.bitso_bitcoin import LoadBitsoBitcoin
from src.data.collector.bitypreco_bitcoin import LoadBityBitcoin
from src.data.collector.bitcoin_to_you import LoadBitcoinToYou
from src.data.collector.mercado_bitcoin import LoadMercadoBitcoin
from src.data.collector.ripio_bitcoin import LoadRipioTrade
from src.data.collector.bitfinex_bitcoin import LoadBitfinex
from src.data.collector.foxbit_bitcoin import LoadFoxbitBitcoin
from src.data.collector.gemini_bitcoin import LoadGeminiTrade

from src.functions.filter_corretoras import filter_corretora
from src.functions.change_types import change_types
from src.functions.quantity_order import calcular_quantidade_ordens

import plotly.graph_objects as go
import plotly.express as px

# Configurando a página do Streamlit
st.set_page_config(
    layout="wide",
    page_title="Análise Geral por Visualização Gráfica 📊",
    page_icon="📊"
)

# Título da página
st.title("Análise Geral por Visualização Gráfica 📊")

# Carregar dados de diferentes corretoras
lbb = LoadBrasilBitcoin()
lbitso = LoadBitsoBitcoin()
lbity = LoadBityBitcoin()
ltyou = LoadBitcoinToYou()
lmerc = LoadMercadoBitcoin()
lripio = LoadRipioTrade()
lfox = LoadFoxbitBitcoin()
#lbinex = LoadBitfinex()
#lgemini = LoadGeminiTrade()

# Obter dados de cada corretora
ob_brasil_bitcoin = lbb.get_brasil_bitcoin_orderbook()
ob_bitso_bitcoin = lbitso.get_bitso_bitcoin_orderbook()
ob_bity_bitcoin = lbity.get_bity_bitcoin_orderbook()
ob_to_you = ltyou.get_btou_bitcoin_orderbook()
ob_mercado_bit = lmerc.get_mercado_bitcoin_orderbook()
ob_ripio = lripio.get_ripio_bitcoin_orderbook()
ob_fox = lfox.get_foxbit_bitcoin_orderbook()
#ob_binex = lbinex.get_bitfinex_bitcoin_orderbook()
#ob_gemini = lgemini.get_gemini_bitcoin_orderbook()

# Consolidar os dados de todas as corretoras
orderbook = pd.concat([ob_brasil_bitcoin,  ob_bity_bitcoin,  ob_mercado_bit, ob_ripio, ob_fox], ignore_index=True)

# Filtrar as corretoras selecionadas pelo usuário
orderbook = change_types(orderbook)
corretora = st.sidebar.multiselect(
        "Selecione a corretora desejada",
        options= orderbook['empresa'].unique()
    )

orderbook = filter_corretora(orderbook, corretora)

# Configurar a variação de preço
var_price = st.sidebar.radio(
    "Variação de Preço",
    [0.1, 0.5, 1, 5, 10])

image_url = "../src/images/bitcoin2.jpeg"
st.sidebar.image(image_url, use_column_width=True)

# Dividir os dados em ordens de compra e venda
orderbook_compra = orderbook.loc[orderbook['compra_venda'] == 'compra'].sort_values(by=['preco', 'empresa'], ascending=False).reset_index(drop=True)
orderbook_venda = orderbook.loc[orderbook['compra_venda'] == 'venda'].sort_values(by=['preco', 'empresa'], ascending=True).reset_index(drop=True)

orderbook_compra['Buy'] = orderbook_compra.groupby('empresa')['quantidade'].cumsum()
orderbook_venda['Sell'] = orderbook_venda.groupby('empresa')['quantidade'].cumsum()

st.subheader(f"Análise da Carteira de Pedidos Cumulativa:")

# Plotar a compra cumulativa por empresa
empresas = orderbook_compra['empresa'].unique()
fig_compra, ax = plt.subplots(figsize=(10, 6))
ax.set_title('Compra Cumulativa por Empresa')
ax.set_xlabel('Preço')
ax.set_ylabel('Compra Cumulativa')

for empresa in empresas:
    subset = orderbook_compra[orderbook_compra['empresa'] == empresa]
    ax.fill_between(subset['preco'], subset['Buy'], alpha=0.7, label=f'Compra - {empresa}')
ax.legend()

# Plotar a venda cumulativa por empresa
empresas_venda = orderbook_venda['empresa'].unique()
fig_venda, ax = plt.subplots(figsize=(10, 6))
ax.set_title('Venda Cumulativa por Empresa')
ax.set_xlabel('Preço')
ax.set_ylabel('Venda Cumulativa')

# Plotar para cada empresa
for empresa in empresas_venda:
    subset = orderbook_venda[orderbook_venda['empresa'] == empresa]
    ax.fill_between(subset['preco'], subset['Sell'], alpha=0.7, label=f'Sell - {empresa}')

# Adicionar legenda e exibir o gráfico
ax.legend()

# # # Organizar os gráficos em duas colunas
col1, col2 = st.columns(2)

# # # Adicionar o gráfico de compra à primeira coluna
with col1:
    st.subheader("Compra")
    st.area_chart(orderbook_compra.rename(columns={'preco': 'Preço', 'Buy': 'Compra'}), x="Preço", y="Compra", color='empresa')
    plt.xlabel("Preço")

# # # Adicionar o gráfico de venda à segunda coluna
with col2:
    st.subheader("Venda")
    st.area_chart(orderbook_venda.rename(columns={'preco': 'Preço', 'Sell': 'Venda'}), x="Preço", y="Venda", color='empresa')


# # Adicionar a subseção para os gráficos de barras
st.subheader("Quantidade Necessária para Mudar o Preço em " + str(var_price) + '%' )

df_qtd_compra = calcular_quantidade_ordens(orderbook_compra, var_price).sort_values('qtd_ordens', ascending=True)
df_qtd_venda = calcular_quantidade_ordens(orderbook_venda, var_price).sort_values('qtd_ordens', ascending=False)

print(df_qtd_compra)

col3, col4 = st.columns(2)
with col3:
    st.subheader("Compra")
    st.bar_chart(df_qtd_compra.rename(columns={'empresa': 'Empresa', 'qtd_ordens': 'Quantidade de Ordens'}), x="Empresa", y="Quantidade de Ordens", color="Empresa")
with col4:
    st.subheader("Venda")
    st.bar_chart(df_qtd_venda.rename(columns={'empresa': 'Empresa', 'qtd_ordens': 'Quantidade de Ordens'}), x="Empresa", y="Quantidade de Ordens", color="Empresa")



# st.subheader("Visualização Tabular dos Dados:")


# st.write(orderbook)