from config import Settings
from modules import DataFetcher, AdvancedTrader
from core.risk_management.manager import RiskManager
import logging
from typing import List, Dict

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self):
        """تهيئة مكونات البوت"""
        self.data_fetcher = DataFetcher()
        self.trader = AdvancedTrader(
            Settings.BINANCE_API_KEY,
            Settings.BINANCE_SECRET
        )
        self.risk_manager = RiskManager(
            max_drawdown=0.05,  # 5% سحب أقصى
            risk_per_trade=0.01  # 1% مخاطرة لكل صفقة
        )

    def analyze_market(self, symbol: str) -> Dict:
        """تحليل بيانات السوق"""
        data = self.data_fetcher.get_ohlcv(symbol)
        if not data:
            raise ValueError(f"فشل جلب بيانات {symbol}")
        
        # هنا يمكنك إضافة منطق التحليل الخاص بك
        return {
            'symbol': symbol,
            'price': data[-1][4],  # آخر سعر إغلاق
            'trend': 'up' if data[-1][4] > data[-2][4] else 'down'
        }

    def execute_trade(self, symbol: str, analysis: Dict):
        """تنفيذ صفقة مع إدارة المخاطر"""
        try:
            # حساب حجم المركز الآمن
            balance = self.trader.get_balance('USDT')
            position_size = self.risk_manager.calculate_position_size(
                portfolio_value=balance,
                stop_loss_pct=2  # وقف خسارة 2%
            )
            
            if self.risk_manager.validate_trade(0.03):  # 3% drawdown حالى
                side = 'buy' if analysis['trend'] == 'up' else 'sell'
                
                logger.info(f"تنفيذ صفقة: {side} {symbol} بحجم {position_size:.6f}")
                
                # تنفيذ الصفقة الفعلية (إلغاء التعليق للاستخدام الحقيقي)
                # order = self.trader.execute_order(
                #     symbol=symbol,
                #     side=side,
                #     amount=float(position_size),
                #     order_type='market'
                # )
                # return order
                
                # للإغراض التوضيحية فقط:
                return {
                    'status': 'simulated',
                    'symbol': symbol,
                    'side': side,
                    'amount': float(position_size)
                }
            else:
                logger.warning("تم تجاوز حد السحب الأقصى، لا توجد صفقات جديدة")
                return None
                
        except Exception as e:
            logger.error(f"خطأ في تنفيذ الصفقة: {e}", exc_info=True)
            raise

def main():
    bot = TradingBot()
    
    try:
        # تحليل السوق
        analysis = bot.analyze_market('BTC/USDT')
        logger.info(f"تحليل السوق: {analysis}")
        
        # تنفيذ الصفقة
        trade_result = bot.execute_trade('BTC/USDT', analysis)
        if trade_result:
            logger.info(f"نتيجة الصفقة: {trade_result}")
        else:
            logger.info("لم يتم تنفيذ أي صفقة")
            
    except Exception as e:
        logger.critical(f"فشل تشغيل البوت: {e}", exc_info=True)

if __name__ == "__main__":
    main()