import requests
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))


class LoadMercadoBitcoin():

    def get_mercado_bitcoin_orderbook(self):

        url = 'https://api.mercadobitcoin.net/api/v4/BTC-BRL/orderbook?limit=100'
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            df_mercado_bitcoin = self.organiza_dados(data)
            
            return df_mercado_bitcoin
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados do Mercado Bitcoin: {e}")
            return None


    def organiza_dados(self, data):

        buy_orders = pd.DataFrame(data['bids'], columns=['preco', 'quantidade'])
        sell_orders = pd.DataFrame(data['asks'],  columns=['preco', 'quantidade'])

        buy_orders['compra_venda'] = 'compra'
        sell_orders['compra_venda'] = 'venda'
        df_bitcoin = pd.concat([buy_orders,sell_orders])

        df_bitcoin['empresa'] = 'Mercado Bitcoin'
       
        return df_bitcoin[['preco', 'quantidade', 'compra_venda', 'empresa']]