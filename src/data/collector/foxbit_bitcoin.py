import requests
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))


class LoadFoxbitBitcoin():

    def get_foxbit_bitcoin_orderbook(self):

        url = 'https://api.foxbit.com.br/rest/v3/markets/BTCBRL/orderbook'
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            df_foxbit = self.organiza_dados(data)
            
            return df_foxbit
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados da Foxbit: {e}")
            return None


    def organiza_dados(self, data):

        buy_orders = pd.DataFrame(data['bids'], columns=['preco', 'quantidade'])
        sell_orders = pd.DataFrame(data['asks'],  columns=['preco', 'quantidade'])

        buy_orders['compra_venda'] = 'compra'
        sell_orders['compra_venda'] = 'venda'
        df_bitcoin = pd.concat([buy_orders,sell_orders])

        df_bitcoin['empresa'] = 'Foxbit'
       
        return df_bitcoin[['preco', 'quantidade', 'compra_venda', 'empresa']]
    

# lg = LoadFoxbitBitcoin()
# ob = lg.get_foxbit_bitcoin_orderbook()
# print(ob.head())