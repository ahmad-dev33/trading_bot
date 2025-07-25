import pytest
from core.risk_management.manager import RiskManager

class TestRiskManager:
    @pytest.fixture
    def manager(self):
        return RiskManager(max_drawdown=0.05, risk_per_trade=0.01)

    def test_position_size_calculation(self, manager):
        # اختبار حساب حجم المركز
        size = manager.calculate_position_size(
            portfolio_value=10000,
            stop_loss_pct=2  # 2%
        )
        assert float(size) == pytest.approx(5.0)  # 1% من 10000 / 2%

    def test_drawdown_validation(self, manager):
        assert manager.validate_trade(0.04) is True
        assert manager.validate_trade(0.06) is False