import yfinance as yf

def get_stock_price(ticker):
    data = yf.Ticker(ticker).history(period="1mo").iloc[-1].Close
    return str(data)

if __name__ == '__main__':
    print(get_stock_price("AAPL"))
