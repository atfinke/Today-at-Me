import requests
from datetime import datetime

from components import cache, logging
from configuration import config

logger = logging.setup_logger(
    'stocks', config.STOCKS_LOGGING_PATH)

memory_cache = None

def fetch_stocks(force_cache=False):
    global memory_cache

    if memory_cache:
        logger.info('fetch_stocks: checking memory cache')
        if force_cache:
            logger.info('fetch_stocks: force cache')
            return memory_cache[config.CACHE_CONTENT_KEY]

    content = cache.content(memory_cache, config.STOCKS_CACHE_LIFETIME, False)
    if content:
        return content

    try:
        logger.info('fetch_stocks: using remote')
        stocks = []
        symbols = config.STOCKS_SYMBOLS
        for symbol in symbols:
            stocks.append({'name': symbol, 'percent': _nasdaq_stock_percent_change(symbol)})

        stocks.extend(_exchanges())

        cache_dict = {
            config.CACHE_DATE_KEY: datetime.now().timestamp(),
            config.CACHE_CONTENT_KEY: stocks
        }
        memory_cache = cache_dict
        return stocks
    except:
        return None

def _nasdaq_stock_percent_change(symbol):
    endpoint = 'https://api.nasdaq.com/api/quote/' + symbol + '/info?assetclass=stocks'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    response = requests.get(endpoint, headers=headers, timeout=5).json()
    data = response['data']

    if 'secondaryData' in data and data['secondaryData']:
        data = data['secondaryData']
    else:
        data = data['primaryData']
    return data['percentageChange'].strip().replace(' ', '')
    
def _exchanges():
    exchanges = []
    endpoint = 'https://api.nasdaq.com/api/quote/indices?symbol=IXIC&symbol=SPX'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    response = requests.get(endpoint, headers=headers, timeout=5).json()
    data = response['data']
    
    for exchange in data:
        name = exchange['companyName'].replace('Composite', '')
        percent = exchange['percentageChange'].strip().replace(' ', '')
        percent = percent if percent[0] == '-' else ('+' + percent)
        exchanges.append({'name': name, 'percent': percent})
    exchanges = sorted(exchanges, key = lambda i: i['name'])
    return exchanges