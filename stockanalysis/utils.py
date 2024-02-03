import requests
from bs4 import BeautifulSoup

def scrape_stock_data(symbol, exchange):
    if exchange == "NASDAQ":
        url =  f"https://finance.yahoo.com/quote/{symbol}"
    elif exchange == "NSE":
        symbol = symbol + ".NS"
        url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch"
        # url = "https://finance.yahoo.com/quote/TATAMOTORS.NS?p=TATAMOTORS.NS&.tsrc=fin-srch"


    headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:

            soup = BeautifulSoup(response.content, 'html.parser')
            current_price = soup.find("fin-streamer", {"data-symbol": f"{symbol}"})['value']
            price_changed = soup.find("fin-streamer", {"data-symbol": f"{symbol}", 'data-test':'qsp-price-change'}).span.text
            percentage_changed = soup.find("fin-streamer", {"data-symbol": f"{symbol}", 'data-field':'regularMarketChangePercent'}).span.text
            privious_close = soup.find('td', {'data-test': 'PREV_CLOSE-value'}).text
            week_52_range = soup.find('td', {'data-test': 'FIFTY_TWO_WK_RANGE-value'}).text
            week_52_low, week_52_high = week_52_range.split(' - ')
            market_cap = soup.find('td', {'data-test': 'MARKET_CAP-value'}).text
            pe_ratio = soup.find('td', {'data-test': 'PE_RATIO-value'}).text
            divident_yield = soup.find('td', {'data-test': 'DIVIDEND_AND_YIELD-value'}).text

            return {
                "current_price":current_price,
                "price_changed":price_changed,
                "percentage_changed":percentage_changed,
                "previous_close":privious_close,
                "week_52_high":week_52_high,
                "week_52_low":week_52_low,
                "market_cap":market_cap,
                "pe_ratio":pe_ratio,
                "divident_yield":divident_yield
            }

        else:
            return "Please enter valid symbol"
    except Exception as E:
        print(f"Internal Server Error", E)
        return None

scrape_stock_data('TATAMOTORS', 'NSE')