import yfinance as yf
import pandas as pd

'''
# ENTREPRISES
Apple Inc. (AAPL) - Symbole boursier pour Apple.
Microsoft Corporation (MSFT) - Symbole boursier pour Microsoft.
Alphabet Inc. (GOOGL) - Symbole boursier pour Alphabet (maison mère de Google).
Amazon.com, Inc. (AMZN) - Symbole boursier pour Amazon.
Facebook, Inc. (FB) - Symbole boursier pour Facebook.

# CRYPTOMONNAIE
Bitcoin (BTC) - La première et la plus connue des cryptomonnaies.
Ethereum (ETH) - Une plateforme blockchain populaire et une cryptomonnaie.
Ripple (XRP) - Connu pour son réseau de transfert de fonds basé sur la technologie blockchain.
Litecoin (LTC) - Une cryptomonnaie similaire à Bitcoin mais avec des transactions plus rapides.
Cardano (ADA) - Une plateforme blockchain qui vise à fournir un environnement plus sécurisé et durable pour les contrats intelligents.

'''


# Récupère les données de Yahoo Finance
def save_stock_data_to_csv(ticker, start_date, end_date, output_file):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data.to_csv(output_file)


if __name__ == "__main__":
    ticker_symbol = "BTC" # ex: AAPL pour Apple
    start_date = "2022-01-01"
    end_date = "2022-12-31"

    output_csv_file = "Courbes/stock_data_" + ticker_symbol + ".csv"
    save_stock_data_to_csv(ticker_symbol, start_date, end_date, output_csv_file)
