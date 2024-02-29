import pandas as pd

def filter_corretora(orderbook, corretoras = []):
    if len(corretoras) > 0:
        orderbook = orderbook.loc[orderbook['empresa'].isin(corretoras)]
    return orderbook