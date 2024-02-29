import streamlit as st
from PIL import Image

# Definindo o título e ícone da página
st.set_page_config(
    page_title="Análise de Bitcoin",
    page_icon="🪙"
)

# Definindo o título e ícone da barra lateral
st.sidebar.markdown("# Análise de Bitcoin 🪙")
st.sidebar.markdown("""___""")

# Definindo o título principal do dashboard
st.write("# Dashboard para Análise e Visualização de Bitcoin 🪙")

# Descrição do dashboard
st.markdown(
    """
    ##### Painel idealizado para visualização gráfica de dados sobre Ordens de Compra e Venda de criptomoedas, assim como a variação percentual no preço mediante a compra de uma certa quantidade de criptomoedas.
    """
)