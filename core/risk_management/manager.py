from decimal import Decimal
from typing import Dict

class RiskManager:
    def __init__(self, max_drawdown: float = 0.05, risk_per_trade: float = 0.01):
        """
        :param max_drawdown: الحد الأقصى المسموح به للخسارة (5%)
        :param risk_per_trade: نسبة المخاطرة لكل صفقة (1%)
        """
        self.max_drawdown = Decimal(str(max_drawdown))
        self.risk_per_trade = Decimal(str(risk_per_trade))

    def calculate_position_size(self, 
                             portfolio_value: float, 
                             stop_loss_pct: float) -> Decimal:
        """
        حساب حجم المركز الآمن
        
        :param portfolio_value: القيمة الإجمالية للمحفظة
        :param stop_loss_pct: نسبة وقف الخسارة (بالنسبة المئوية)
        :return: حجم المركز المقترح
        """
        if stop_loss_pct <= 0:
            raise ValueError("يجب أن تكون نسبة وقف الخسارة موجبة")
            
        portfolio_dec = Decimal(str(portfolio_value))
        stop_loss_dec = Decimal(str(stop_loss_pct/100))
        
        risk_amount = portfolio_dec * self.risk_per_trade
        return (risk_amount / stop_loss_dec).quantize(Decimal('0.000001'))

    def validate_trade(self, current_drawdown: float) -> bool:
        """التحقق من عدم تجاوز الحد الأقصى للخسارة"""
        return current_drawdown < float(self.max_drawdown)