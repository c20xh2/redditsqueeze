import yfinance as yf

def get_ticker_info(ticker_name):
    try:
        ticker = yf.Ticker(ticker_name)
        validate = ticker.fast_info['last_price']
        return ticker
    except Exception as e:
        return None
