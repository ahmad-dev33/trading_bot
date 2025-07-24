from core.hf_integration import create_hf_integration
from config.settings import Settings
import logging

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_hf_integration():
    try:
        # 1. تهيئة الوحدة
        hf = create_hf_integration(
            model_name=Settings.HF_MODEL_NAME,
            hf_token=Settings.HF_API_TOKEN,
            device="auto"
        )
        
        if not hf:
            raise RuntimeError("فشل تهيئة وحدة HF")

        # 2. مثال تحليل سوق
        market_prompt = """
        حلل بيانات السوق التالية وقدم توصية:
        - زوج: BTC/USDT
        - سعر حالى: $51,200
        - RSI (14): 67
        - تغير 24h: +2.3%
        - دعم رئيسي: $50,000
        - مقاومة: $52,000
        
        المطلوب:
        - توصية: [شراء/بيع/انتظار]
        - ثقة: [0-100%]
        - سبب فني مختصر
        """
        
        # 3. توليد النص
        result = hf.generate_text(
            prompt=market_prompt,
            generation_params={
                "max_new_tokens": 200,
                "temperature": 0.5
            }
        )
        
        # 4. عرض النتائج
        if result["status"] == "success":
            print("\n🎯 التوصية:\n", result["text"])
            print("\n⚡ معطيات الأداء:")
            print(f"- الجهاز: {result['metrics']['device']}")
            print(f"- الوقت: {result['metrics']['latency_seconds']} ثانية")
            print(f"- عدد الكلمات: {result['metrics']['tokens_generated']}")
        else:
            print("❌ فشل:", result["message"])

    except Exception as e:
        logging.error(f"حدث خطأ أثناء الاختبار: {e}", exc_info=True)

if __name__ == "__main__":
    test_hf_integration()