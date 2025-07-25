import streamlit as st
from config import Settings
from core.risk_management.manager import RiskManager
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(
    page_title="Trading Bot Dashboard",
    layout="wide"
)

def main():
    st.title("🧠 Trading Bot Dashboard")
    
    # قسم الإعدادات
    with st.sidebar:
        st.header("⚙️ الإعدادات")
        api_key = st.text_input("Binance API Key", type="password")
        api_secret = st.text_input("Binance API Secret", type="password")
        model_name = st.selectbox(
            "النموذج", 
            ["microsoft/phi-2", "google/gemma-7b", "facebook/opt-1.3b"]
        )
    
    # قسم التحليل
    st.header("📊 تحليل السوق")
    col1, col2 = st.columns(2)
    
    with col1:
        symbol = st.selectbox("اختر زوج التداول", ["BTC/USDT", "ETH/USDT", "SOL/USDT"])
        timeframe = st.selectbox("الإطار الزمني", ["1m", "15m", "1h", "4h", "1d"])
        
    with col2:
        risk = st.slider("نسبة المخاطرة %", 0.1, 5.0, 1.0, step=0.1)
        stop_loss = st.slider("وقف الخسارة %", 0.5, 10.0, 2.0, step=0.5)
    
    # محاكاة بيانات (استبدل ببيانات حقيقية)
    data = pd.DataFrame({
        "time": pd.date_range(start="2024-01-01", periods=100),
        "price": [100 + i + (i * 0.1) for i in range(100)]
    })
    
    # عرض الرسم البياني
    fig = px.line(data, x="time", y="price", title=f"سعر {symbol}")
    st.plotly_chart(fig, use_container_width=True)
    
    # قسم إدارة المخاطر
    st.header("🛡️ إدارة المخاطر")
    if st.button("حساب حجم المركز"):
        risk_manager = RiskManager(risk_per_trade=risk/100)
        size = risk_manager.calculate_position_size(
            portfolio_value=10000,  # يمكن استبدالها بالقيمة الفعلية
            stop_loss_pct=stop_loss
        )
        st.success(f"حجم المركز المقترح: {size:.4f} {symbol.split('/')[0]}")
    
    # قسم التوصيات
    st.header("💡 التوصيات")
    if st.button("إنشاء توصية"):
        with st.spinner("جاري التحليل..."):
            # هنا تكامل مع نموذج Hugging Face
            recommendation = {
                "action": "شراء",
                "confidence": 75,
                "target": data["price"].iloc[-1] * 1.05,
                "stop_loss": data["price"].iloc[-1] * 0.98
            }
            st.json(recommendation)

if __name__ == "__main__":
    main()