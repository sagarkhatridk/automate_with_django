import requests
from bs4 import BeautifulSoup

def scrape_stock_data(symbol,exchange):
    if exchange == "NASDAQ":
        url =  f"https://finance.yahoo.com/quote/{symbol}"
    elif exchange == "NSE":
        symbol = symbol + ".NS"
        url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch"
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.content, 'html.parser')
    current_price = soup.find(f"fin-streamer", {"data-symbol": {symbol}})['value']
    print('current_price: ', current_price)
    privious_close = soup.find('td', {'data-test': 'PREV_CLOSE-value'}).text
    print('privious_close: ', privious_close)



scrape_stock_data('TATAMOTORS', 'NSE')