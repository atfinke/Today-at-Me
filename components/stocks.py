import urllib.request, json 
from datetime import datetime

from components import logging
from configuration import config

logger = logging.setup_logger(
    'stocks', config.STOCKS_LOGGING_PATH)

memory_cache = None

def fetch_stocks():
    global memory_cache

    existing_cache = memory_cache
    if existing_cache:
        logger.info('fetch_stocks: checking memory cache')

    if existing_cache:
        date = existing_cache[config.CACHE_DATE_KEY]
        if datetime.now().timestamp() < date + config.STOCKS_CACHE_LIFETIME:
            logger.info('fetch_stocks: using cache')
            return existing_cache[config.CACHE_CONTENT_KEY]
        else:
            logger.info('fetch_stocks: cache too old {}'.format(datetime.now().timestamp() - date))

    stocks = []
    symbols = ['AAPL', 'MSFT']
    for symbol in symbols:
        stocks.append({'name': symbol, 'percent': _nasdaq_stock_percent_change(symbol)})

    stocks.extend(_exchanges())

    cache_dict = {
        config.CACHE_DATE_KEY: datetime.now().timestamp(),
        config.CACHE_CONTENT_KEY: stocks
    }
    memory_cache = cache_dict

    return stocks

def _nasdaq_stock_percent_change(symbol):
    endpoint = 'https://api.nasdaq.com/api/quote/' + symbol + '/info?assetclass=stocks'
    with urllib.request.urlopen(endpoint) as url:
        data = json.loads(url.read().decode())['data']['primaryData']
        sign = '-' if data['deltaIndicator'] == 'down' else '+'
        return sign + data['percentageChange'].strip().replace(' ', '')
    return None
    
def _exchanges():
    exchanges = []
    endpoint = 'https://api.nasdaq.com/api/quote/indices?symbol=IXIC&symbol=SPX'
    with urllib.request.urlopen(endpoint) as url:
        data = json.loads(url.read().decode())['data']
        for exchange in data:
            name = exchange['companyName'].replace('Composite', '')
            exchanges.append({'name': name, 'percent': exchange['percentageChange'].strip().replace(' ', '')})
    exchanges = sorted(exchanges, key = lambda i: i['name'])
    return exchanges