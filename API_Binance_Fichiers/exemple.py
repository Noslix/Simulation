import ccxt
import time

# Paramètres
api_key = 'votre_api_key'
api_secret = 'votre_api_secret'
symbol = 'BTC/USDT'  # Paire de trading
amount = 0.01  # Montant de BTC à acheter
take_profit_ratio = 1.05  # Prendre le profit à +5%
stop_loss_ratio = 0.95  # Stop loss à -5%
trailing_stop = True
trailing_distance = 0.02  # Distance du suiveur de stop-loss

# Initialisation
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})
exchange.load_markets()

# Acheter
order = exchange.create_market_buy_order(symbol, amount)
print(f"Achat effectué à {order['price']} USDT")

# Prix d'achat
buy_price = float(order['price'])

# Initialiser les niveaux de Take Profit et de Stop Loss
take_profit_price = buy_price * take_profit_ratio
stop_loss_price = buy_price * stop_loss_ratio

while True:
    time.sleep(10)
    ticker = exchange.fetch_ticker(symbol)
    current_price = ticker['last']

    # Vérifier les conditions pour vendre
    if current_price >= take_profit_price:
        print(f"Prix actuel: {current_price}, Take Profit à: {take_profit_price}. Vendre!")
        exchange.create_market_sell_order(symbol, amount)
        break
    elif current_price <= stop_loss_price:
        print(f"Prix actuel: {current_price}, Stop Loss à: {stop_loss_price}. Vendre!")
        exchange.create_market_sell_order(symbol, amount)
        break

    # Mise à jour du Stop Loss avec suiveur
    if trailing_stop and current_price > buy_price:
        new_stop_loss_price = current_price * (1 - trailing_distance)
        if new_stop_loss_price > stop_loss_price:
            print(f"Mise à jour du Stop Loss à {new_stop_loss_price}")
            stop_loss_price = new_stop_loss_price
