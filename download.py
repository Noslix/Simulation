import yfinance as yf
import pandas as pd

# Récupère les données de Yahoo Finance
def save_stock_data_to_csv(ticker, start_date, end_date, output_file):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data.to_csv(output_file)


if __name__ == "__main__":
    ticker_symbol = "AAPL" # ex: AAPL pour Apple
    start_date = "2022-01-01"
    end_date = "2022-12-31"

    output_csv_file = "Courbes/stock_data_" + ticker_symbol + ".csv"
    save_stock_data_to_csv(ticker_symbol, start_date, end_date, output_csv_file)
