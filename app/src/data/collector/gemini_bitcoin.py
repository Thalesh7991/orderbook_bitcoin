import requests
import pandas as pd

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))


class LoadGeminiTrade():

    def get_gemini_bitcoin_orderbook(self):

        base_url = "https://api.gemini.com/v1"
        
        try:
            response = requests.get(base_url + "/book/btcusd")
            response.raise_for_status()

            data = response.json()
            df_gemini_bitcoin = self.organiza_dados(data)

            return df_gemini_bitcoin
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados do Gemini Trade: {e}")
            return None
    
    def organiza_dados(self, data):
        buy_orders = data['bids']
        sell_orders = data['asks']

        buy_orders = pd.DataFrame(data['bids'])
        sell_orders = pd.DataFrame(data['asks'])

        buy_orders['compra_venda'] = 'compra'
        sell_orders['compra_venda'] = 'venda'

        df_gemini_bitcoin = pd.concat([buy_orders,sell_orders])
        df_gemini_bitcoin.rename(columns={"price": "valor", "amount": "quantidade"}, inplace=True)
        df_gemini_bitcoin = df_gemini_bitcoin.drop(columns=['timestamp'])
        df_gemini_bitcoin['empresa'] = 'Gemini'

        # Converter as colunas 'valor' e 'quantidade' para números (float)
        df_gemini_bitcoin['valor'] = pd.to_numeric(df_gemini_bitcoin['valor'])
        df_gemini_bitcoin['quantidade'] = pd.to_numeric(df_gemini_bitcoin['quantidade'])

        # Adicionar a coluna 'preço'
        df_gemini_bitcoin['preço'] = df_gemini_bitcoin['valor'] / df_gemini_bitcoin['quantidade']
        df_gemini_bitcoin.drop('valor', axis=1)

        return df_gemini_bitcoin[['preço', 'quantidade', 'compra_venda', 'empresa']]

# lg = LoadGeminiTrade()
# ob = lg.get_gemini_bitcoin_orderbook()
# print(ob.head())


