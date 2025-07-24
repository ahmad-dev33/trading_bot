from ccxt import binance
import time

class Trader:
    def __init__(self, api_key, secret):
        self.exchange = binance({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True  # مهم لمنع تجاوز حد الطلبات
        })
    
    def execute_order(self, symbol, side, amount, max_retries=3):
        """
        تنفيذ أمر تداول مع معالجة الأخطاء
        
        :param symbol: زوج التداول (مثال: 'BTC/USDT')
        :param side: نوع الأمر ('buy'/'sell')
        :param amount: الكمية
        :param max_retries: عدد المحاولات عند الفشل
        :return: نتيجة التنفيذ أو None إذا فشل
        """
        for attempt in range(max_retries):
            try:
                order = self.exchange.create_order(
                    symbol=symbol,
                    type='market',
                    side=side,
                    amount=amount
                )
                return order
                
            except ccxt.NetworkError as e:
                print(f"خطأ في الشبكة (المحاولة {attempt + 1}): {e}")
                time.sleep(2)  # انتظر قبل إعادة المحاولة
                
            except ccxt.ExchangeError as e:
                print(f"خطأ من البورصة: {e}")
                break
                
            except Exception as e:
                print(f"خطأ غير متوقع: {e}")
                break
                
        return None

    def get_balance(self, currency='USDT'):
        """جلب رصيد عملة معينة"""
        try:
            balance = self.exchange.fetch_balance()
            return balance['total'].get(currency, 0)
        except Exception as e:
            print(f"خطأ في جلب الرصيد: {e}")
            return 0