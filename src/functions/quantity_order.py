import pandas as pd

def calcular_quantidade_ordens(orderbook, percentual):
    dict_ordens = {
        'empresa': [],
        'qtd_ordens': []
    }
    empresas = orderbook['empresa'].unique()

    for empresa in empresas:
        ob = orderbook.loc[orderbook['empresa'] == empresa]
        
        mean_price = ob['preco'].mean()
        top_price = mean_price + (mean_price * (percentual/100) )
        bottom_price = mean_price - (mean_price * (percentual/100) )
        qtd_ordens = ob.loc[(ob['preco'] > bottom_price) & (ob['preco'] < top_price)].shape[0]

        # Adicionar dados ao dicionário
        dict_ordens['empresa'].append(empresa)
        dict_ordens['qtd_ordens'].append(qtd_ordens)
        

    df_ordens = pd.DataFrame(dict_ordens)
    return df_ordens