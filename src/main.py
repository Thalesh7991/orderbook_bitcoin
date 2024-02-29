from data.collector.brasil_bitcoin import LoadBrasilBitcoin

lbb = LoadBrasilBitcoin()
orderbook_data = lbb.get_brasil_bitcoin_orderbook()

print(orderbook_data)