import requests
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))


class LoadBitfinex():
    def get_bitfinex_bitcoin_orderbook(self):

        url = "https://api-pub.bitfinex.com/v2/trades/tBTCUSD/hist?limit=10000&sort=-1"

        try:
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            df_bitfinex_bitcoin = self.organiza_dados(data)
            
            return df_bitfinex_bitcoin
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados da Bitfinex: {e}")
            return None
    
    def organiza_dados(self, data):
        # Separação de compras e vendas
        buy_orders = [trade for trade in data if trade[2] > 0]
        sell_orders = [trade for trade in data if trade[2] < 0]

        # Criar dataframes
        df_buy = pd.DataFrame(buy_orders, columns=["id", "MTS", "AMOUNT", "PRICE"])
        df_sell = pd.DataFrame(sell_orders, columns=["id", "MTS", "AMOUNT", "PRICE"])

        # Adicionar coluna 'compra_venda'
        df_buy["compra_venda"] = "compra"
        df_sell["compra_venda"] = "venda"

        # Concatenar dataframes
        df_bitfinex_bitcoin = pd.concat([df_buy, df_sell], ignore_index=True)
        df_bitfinex_bitcoin['empresa'] = 'Bitfinex'

        # Renomear as colunas
        df_bitfinex_bitcoin.rename(columns={"MTS": "preco", "AMOUNT": "quantidade", "PRICE": "valor"}, inplace=True)
        
        # Selecionar apenas as colunas desejadas
        df_bitfinex_bitcoin = df_bitfinex_bitcoin[['preco', 'quantidade', 'compra_venda', 'empresa']]

        return df_bitfinex_bitcoin



# lg = LoadBitfinex()
# ob = lg.get_bitfinex_bitcoin_orderbook()
# print(ob.head())