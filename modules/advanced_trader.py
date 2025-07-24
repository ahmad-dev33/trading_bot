from ccxt import binance
import time
import logging
from typing import Optional, Dict, Union

class AdvancedTrader:
    def __init__(self, api_key: str, secret: str):
        """
        Initialize trading bot with API credentials
        
        :param api_key: Binance API key
        :param secret: Binance API secret
        """
        self.exchange = binance({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
            'options': {
                'adjustForTimeDifference': True
            }
        })
        logging.basicConfig(
            filename='trading_log.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def execute_order(self, 
                    symbol: str, 
                    side: str, 
                    amount: float, 
                    order_type: str = 'market',
                    price: Optional[float] = None,
                    max_retries: int = 3,
                    max_amount: float = 1000) -> Optional[Dict]:
        """
        Execute trading order with advanced error handling
        
        :param symbol: Trading pair (e.g. 'BTC/USDT')
        :param side: 'buy' or 'sell'
        :param amount: Order amount
        :param order_type: 'market' or 'limit'
        :param price: Required for limit orders
        :param max_retries: Maximum retry attempts
        :param max_amount: Maximum allowed order amount
        :return: Order details or None if failed
        """
        # Validate inputs
        if amount > max_amount:
            logging.error(f"Amount {amount} exceeds maximum allowed {max_amount}")
            raise ValueError("Order amount exceeds limit")

        if order_type == 'limit' and price is None:
            raise ValueError("Price must be specified for limit orders")

        for attempt in range(max_retries):
            try:
                order_params = {
                    'symbol': symbol,
                    'type': order_type,
                    'side': side,
                    'amount': amount
                }
                
                if order_type == 'limit':
                    order_params['price'] = price
                
                order = self.exchange.create_order(**order_params)
                logging.info(f"Order executed: {order}")
                return order

            except ccxt.NetworkError as e:
                wait_time = 2 ** (attempt + 1)  # Exponential backoff
                logging.warning(f"Network error (attempt {attempt + 1}): {e} - Retrying in {wait_time}s")
                time.sleep(wait_time)
                
            except ccxt.ExchangeError as e:
                logging.error(f"Exchange error: {e}")
                break
                
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                break
                
        return None

    def get_balance(self, currency: str = 'USDT') -> float:
        """
        Get account balance for specified currency
        
        :param currency: Currency symbol (e.g. 'BTC')
        :return: Available balance
        """
        try:
            balance = self.exchange.fetch_balance()
            return float(balance['total'].get(currency, 0))
        except Exception as e:
            logging.error(f"Balance check failed: {e}")
            return 0.0

    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current market price
        
        :param symbol: Trading pair
        :return: Current price or None if failed
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return float(ticker['last'])
        except Exception as e:
            logging.error(f"Price check failed: {e}")
            return None

    def cancel_order(self, order_id: str, symbol: str) -> bool:
        """
        Cancel an existing order
        
        :param order_id: Order ID to cancel
        :param symbol: Trading pair
        :return: True if successful
        """
        try:
            result = self.exchange.cancel_order(order_id, symbol)
            logging.info(f"Order canceled: {order_id}")
            return True
        except Exception as e:
            logging.error(f"Cancel order failed: {e}")
            return False

    def get_order_status(self, order_id: str, symbol: str) -> Optional[Dict]:
        """
        Check order status
        
        :param order_id: Order ID to check
        :param symbol: Trading pair
        :return: Order details or None if failed
        """
        try:
            return self.exchange.fetch_order(order_id, symbol)
        except Exception as e:
            logging.error(f"Order status check failed: {e}")
            return None

    def calculate_risk_amount(self, 
                            capital: float, 
                            risk_pct: float = 1.0, 
                            stop_loss_pct: float = 2.0) -> float:
        """
        Calculate position size based on risk management
        
        :param capital: Total available capital
        :param risk_pct: Risk percentage per trade (1.0 = 1%)
        :param stop_loss_pct: Stop loss percentage
        :return: Position size
        """
        risk_amount = capital * (risk_pct / 100)
        return risk_amount / (stop_loss_pct / 100)

# Example Usage
if __name__ == "__main__":
    trader = AdvancedTrader(api_key="your_api_key", secret="your_secret")
    
    # Get current price
    price = trader.get_current_price('BTC/USDT')
    print(f"Current BTC Price: {price}")
    
    # Calculate position size
    balance = trader.get_balance('USDT')
    amount = trader.calculate_risk_amount(balance)
    print(f"Suggested position size: {amount}")
    
    # Execute trade
    if price and amount:
        order = trader.execute_order(
            symbol='BTC/USDT',
            side='buy',
            amount=amount,
            order_type='market'
        )
        if order:
            print(f"Order successful: {order['id']}")