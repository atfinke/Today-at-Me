import urllib.request, json 
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
    with urllib.request.urlopen(endpoint) as url:
        data = json.loads(url.read().decode())['data']
        
        if 'secondaryData' in data and data['secondaryData']:
            data = data['secondaryData']
        else:
            data = data['primaryData']
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
            percent = exchange['percentageChange'].strip().replace(' ', '')
            percent = percent if percent[0] == '-' else ('+' + percent)
            exchanges.append({'name': name, 'percent': percent})
    exchanges = sorted(exchanges, key = lambda i: i['name'])
    return exchanges