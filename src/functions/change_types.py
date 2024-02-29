import pandas as pd

def change_types(data):
        data['preco'] = data['preco'].astype(float)
        data['quantidade'] = data['quantidade'].astype(float)
        return data