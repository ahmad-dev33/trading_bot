from config import Settings
from modules import DataFetcher, AdvancedTrader

def main():
    # Initialize components
    data_fetcher = DataFetcher()
    trader = AdvancedTrader(Settings.BINANCE_API_KEY, Settings.BINANCE_SECRET)
    
    # Example workflow
    btc_data = data_fetcher.get_ohlcv('BTC/USDT')
    if btc_data:
        print(f"Retrieved {len(btc_data)} candles")
        # Add trading logic here

if __name__ == "__main__":
    main()