import requests
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))


class LoadRipioTrade():

    def get_ripio_bitcoin_orderbook(self):

        url = 'https://api.ripiotrade.co/v4/public/orders/level-3?pair=BTC_BRL'
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            df_ripio = self.organiza_dados(data)
            
            return df_ripio
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados do Ripio Trade: {e}")
            return None


    def organiza_dados(self, data):

        buy_orders = pd.DataFrame(data['data']['bids'])
        sell_orders = pd.DataFrame(data['data']['asks'])

        buy_orders['compra_venda'] = 'compra'
        sell_orders['compra_venda'] = 'venda'

        df_bitcoin = pd.concat([buy_orders,sell_orders])
        df_bitcoin['empresa'] = 'Ripio Trade'

        return df_bitcoin.rename(columns={'price': 'preco', 'amount': 'quantidade'})[['preco', 'quantidade', 'compra_venda', 'empresa']]