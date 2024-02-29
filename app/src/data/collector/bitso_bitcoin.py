import requests
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

class LoadBitsoBitcoin():
    def get_bitso_bitcoin_orderbook(self):
        url = "https://sandbox.bitso.com/api/v3/order_book/?book=btc_brl"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            df_bitso_bitcoin = self.organiza_dados(data)
            
            return df_bitso_bitcoin
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados do Bitso Bitcoin: {e}")
            return None
    
    def organiza_dados(self, data):

        buy_orders = pd.DataFrame(data['payload']['bids'])
        sell_orders = pd.DataFrame(data['payload']['asks'])

        buy_orders['compra_venda'] = 'compra'
        sell_orders['compra_venda'] = 'venda'

        df_bitso_bitcoin = pd.concat([buy_orders,sell_orders])
        df_bitso_bitcoin['empresa'] = 'Bitso Bitcoin'
        df_bitso_bitcoin = df_bitso_bitcoin[['price','amount','compra_venda','empresa']].rename(columns={'price': 'preco','amount':'quantidade'})
        return df_bitso_bitcoin
    



    
#lbb = LoadBitsoBitcoin()
#orderbook_data = lbb.get_bitso_bitcoin_orderbook()

#print(orderbook_data.head())