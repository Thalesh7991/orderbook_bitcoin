import requests
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))


class LoadBitcoinToYou():

    def get_btou_bitcoin_orderbook(self):

        url = 'https://back.bitcointoyou.com/api/v2/orderbook?pair=BTC_BRLC&depth=100'
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            df_b2u = self.organiza_dados(data)
            
            return df_b2u
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados do Bitcoin To You Bitcoin: {e}")
            return None
        
    def organiza_dados(self, data):

        buy_orders = pd.DataFrame(data['bids'], columns=['preco', 'quantidade'])
        sell_orders = pd.DataFrame(data['asks'], columns=['preco', 'quantidade'])

        buy_orders['compra_venda'] = 'compra'
        sell_orders['compra_venda'] = 'venda'

        df_bitcoin = pd.concat([buy_orders, sell_orders])
        df_bitcoin['empresa'] = 'Bitcoin To You'
        

        return df_bitcoin[['preco', 'quantidade', 'compra_venda', 'empresa']]