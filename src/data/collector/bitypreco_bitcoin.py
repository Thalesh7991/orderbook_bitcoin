import requests
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

class LoadBityBitcoin():
    def get_bity_bitcoin_orderbook(self):
        url = "https://api.bitpreco.com/btc-brl/orderbook"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            df_bity_bitcoin = self.organiza_dados(data)
            
            return df_bity_bitcoin
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados do Bity Bitcoin: {e}")
            return None
    
    def organiza_dados(self, data):

        buy_orders = pd.DataFrame(data['bids'])
        sell_orders = pd.DataFrame(data['asks'])

        buy_orders['compra_venda'] = 'compra'
        sell_orders['compra_venda'] = 'venda'

        df_bity_bitcoin = pd.concat([buy_orders,sell_orders])
        df_bity_bitcoin['empresa'] = 'Bity Preço'
        df_bity_bitcoin = df_bity_bitcoin[['price','amount','compra_venda','empresa']].rename(columns={'price': 'preco','amount':'quantidade'})
        return df_bity_bitcoin
    




# lbb = LoadBityBitcoin()
# orderbook_data = lbb.get_bity_bitcoin_orderbook()

# print(orderbook_data.head())