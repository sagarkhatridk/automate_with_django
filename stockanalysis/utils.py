import requests
from parsel import Selector

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

            html_content = Selector(response.text)
            current_price = html_content.xpath(f'//fin-streamer[@data-symbol="{symbol}"][@data-testid="qsp-price"]/@data-value').get('')
            price_changed = "".join(html_content.xpath(f'//fin-streamer[@data-symbol="{symbol}"][@data-testid="qsp-price-change"]/span/text()').getall())
            percentage_changed = html_content.xpath(f'//fin-streamer[@data-symbol="{symbol}"][@data-testid="qsp-price-change-percent"]/@data-value').get('')
            privious_close = html_content.xpath(f'//fin-streamer[@data-symbol="{symbol}"][@data-field="regularMarketPreviousClose"]/@data-value').get('')

            week_52_range = html_content.xpath(f'//fin-streamer[@data-symbol="{symbol}"][@data-field="fiftyTwoWeekRange"]/@data-value').get('')
            print('week_52_range: ', week_52_range)
            week_52_low, week_52_high = week_52_range.split(' - ')
            market_cap = html_content.xpath(f'//fin-streamer[@data-symbol="{symbol}"][@data-field="marketCap"]/@data-value').get('')
            pe_ratio = html_content.xpath(f'//fin-streamer[@data-symbol="{symbol}"][@data-field="trailingPE"]/@data-value').get('')
            divident_yield = html_content.xpath('//span[contains(text(), "Forward Dividend & Yield")]/following-sibling::span[1]/text()').get('')

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