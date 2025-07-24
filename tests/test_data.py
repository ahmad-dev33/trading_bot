import pytest
from modules.data import DataFetcher

class TestDataFetcher:
    @pytest.fixture
    def fetcher(self):
        return DataFetcher(exchange_id='binance')

    def test_get_ohlcv(self, fetcher):
        data = fetcher.get_ohlcv('BTC/USDT', limit=10)
        assert len(data) <= 10