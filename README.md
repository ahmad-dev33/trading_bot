# 📊 Trading Bot with AI Integration

**مشروع بوت تداول ذكي يستخدم تقنيات الذكاء الاصطناعي من Hugging Face لتحليل الأسواق المالية**

## ✨ الميزات الرئيسية

- **تحليل السوق الذكي**: استخدام نماذج Hugging Face المتقدمة لتحليل اتجاهات السوق
- **إدارة المخاطر**: حساب تلقائي لحجم المركز بناء على نسبة المخاطرة
- **دعم متعدد البورصات**: تكامل مع Binance و Bybit (قيد التطوير)
- **واجهة سهلة**: إمكانية التشغيل عبر CLI أو واجهة ويب (قريباً)

## 🛠️ التقنيات المستخدمة

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Hugging Face](https://img.shields.io/badge/Hugging_Face-Transformers-orange)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red)

```text
transformers
torch
pandas
ccxt
python-dotenv
```

## ⚡ البداية السريعة

### المتطلبات المسبقة
- Python 3.10+
- حساب [Hugging Face](https://huggingface.co) مع API Token
- حساب [Binance](https://binance.com) (اختياري)

### التنصيب

1. استنسخ المستودع:
```bash
git clone https://github.com/ahmad-dev33/trading_bot.git
cd trading_bot
```

2. ثبت المتطلبات:
```bash
pip install -r requirements.txt
```

3. إعداد ملف البيئة:
```bash
cp .env.example .env
# عدل ملف .env بإضافة مفاتيح API الخاصة بك
```

4. التشغيل:
```bash
python main.py
```

## 🧠 نموذج الذكاء الاصطناعي

يستخدم المشروع نماذج متقدمة مثل:

- `microsoft/phi-2`
- `google/gemma-7b`

مع إمكانية تخصيص النموذج المستخدم عبر ملف `.env`:

```ini
HF_MODEL_NAME=google/gemma-7b
HF_API_TOKEN=your_token_here
```

## 📊 مثال لتحليل السوق

```python
from core.hf_integration import HFModelHandler

handler = HFModelHandler()
analysis = handler.analyze_market("BTC/USDT 24h data...")
print(analysis)
```

## 🤝 المساهمة في المشروع

1. انشئ Fork للمشروع
2. أنشئ فرعاً جديداً (`git checkout -b feature/your-feature`)
3. أضف Commit للتغييرات (`git commit -m 'Add some feature'`)
4. ارفع الفرع (`git push origin feature/your-feature`)
5. أنشئ Pull Request

## 📜 الرخصة

هذا المشروع مرخص تحت [MIT License](LICENSE).

---

**📬 للتواصل**: [ahmad.dana963@gmail.com](mailto:ahmad.dana963@gmail.com)

**🐞 الإبلاغ عن مشاكل**: [صفحة Issues](https://github.com/ahmad-dev33/trading_bot/issues)

---

<div align="center">
  <img src="https://img.shields.io/github/last-commit/ahmad-dev33/trading_bot" alt="آخر تحديث">
  <img src="https://img.shields.io/github/license/ahmad-dev33/trading_bot" alt="الرخصة">
</div>

> ملاحظة: هذا المشروع لأغراض تعليمية فقط. التداول يحمل مخاطر خسارة رأس المال.
