import ccxt
from typing import List, Dict

class DataFetcher:
    def __init__(self, exchange_id='binance'):
        self.exchange = getattr(ccxt, exchange_id)({
            'rateLimit': 1200,
            'enableRateLimit': True
        })

    def get_ohlcv(self, symbol: str, timeframe='1h', limit=100) -> List[Dict]:
        """Fetch OHLCV data with error handling"""
        try:
            return self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        except ccxt.BaseError as e:
            print(f"Data fetch error: {e}")
            return []