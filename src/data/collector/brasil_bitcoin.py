import requests
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

class LoadBrasilBitcoin():
    def get_brasil_bitcoin_orderbook(self):
        url = "https://brasilbitcoin.com.br/API/orderbook/BTC"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            df_brasil_bitcoin = self.organiza_dados(data)
            
            return df_brasil_bitcoin
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados do Brasil Bitcoin: {e}")
            return None
    
    def organiza_dados(self, data):
        buy_orders = pd.DataFrame(data['buy'])
        sell_orders = pd.DataFrame(data['sell'])

        buy_orders['compra_venda'] = 'compra'
        sell_orders['compra_venda'] = 'venda'

        df_brasil_bitcoin = pd.concat([buy_orders,sell_orders])
        df_brasil_bitcoin['empresa'] = 'Brasil Bitcoin'
        df_brasil_bitcoin = df_brasil_bitcoin[['preco','quantidade','compra_venda','empresa']]
        return df_brasil_bitcoin
    






# # Exemplo de utilização da função
# lbb = LoadBrasilBitcoin()
# orderbook_data = lbb.get_brasil_bitcoin_orderbook()

# print(orderbook_data.head())
