import logging
from typing import Dict, Any, Optional
from transformers import pipeline, AutoTokenizer, GenerationConfig
from huggingface_hub import login, snapshot_download
from pathlib import Path
import torch

class HFIntegration:
    """
    وحدة متكاملة للتعامل مع نماذج Hugging Face
    """
    def __init__(self, 
                model_name: str, 
                hf_token: str, 
                cache_dir: str = "models",
                device: Optional[str] = None):
        """
        تهيئة متقدمة للوحدة
        
        :param model_name: مسار النموذج على HF (مثال: google/gemma-7b-it)
        :param hf_token: توكن الوصول من HF
        :param cache_dir: مسار تخزين النماذج (افتراضي: models/)
        :param device: جهاز التشغيل (cuda/cpu/auto)، None للكشف التلقائي
        """
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.hf_token = hf_token
        self.cache_dir = Path(cache_dir)
        self.device = self._determine_device(device)
        self.model = None
        self.tokenizer = None
        self._setup()

    def _determine_device(self, device: Optional[str]) -> str:
        """تحديد جهاز التشغيل الأمثل"""
        if device:
            return device
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _setup(self):
        """إعداد متقدم للبيئة"""
        try:
            # إنشاء مجلد النماذج بصلاحيات كاملة
            self.cache_dir.mkdir(exist_ok=True, parents=True)
            
            # تسجيل دخول آمن
            login(token=self.hf_token, add_to_git_credential=True)
            self.logger.info("✅ تم المصادقة مع Hugging Face Hub")
            
            # تحميل النموذج
            self._load_model()
            
        except Exception as e:
            self.logger.critical(f"فشل حرج في الإعداد: {e}", exc_info=True)
            raise RuntimeError("تعذر تهيئة وحدة HF") from e

    def _load_model(self):
        """تحميل آمن للنموذج"""
        try:
            self.logger.info(f"⚙️ جاري تحميل النموذج {self.model_name}...")
            
            # تحميل Tokenizer مع معالجة الأخطاء
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                token=self.hf_token,
                cache_dir=str(self.cache_dir),
                trust_remote_code=True
            )
            
            # إعدادات توليد النص
            generation_config = GenerationConfig.from_pretrained(
                self.model_name,
                token=self.hf_token
            )
            
            # تحميل النموذج مع إدارة الذاكرة
            self.model = pipeline(
                task="text-generation",
                model=self.model_name,
                token=self.hf_token,
                device=self.device,
                torch_dtype=torch.float16 if "cuda" in self.device else None,
                model_kwargs={
                    "cache_dir": str(self.cache_dir),
                    "trust_remote_code": True,
                    "low_cpu_mem_usage": True
                },
                generation_config=generation_config
            )
            
            self.logger.info("🎉 تم تحميل النموذج بنجاح")
            
        except Exception as e:
            self.logger.error(f"🔥 خطأ في تحميل النموذج: {e}", exc_info=True)
            raise

    def generate_text(self, 
                    prompt: str, 
                    generation_params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        توليد نص مع معالجة متقدمة للأخطاء
        
        :param prompt: النص المدخل
        :param generation_params: معاملات توليد النص
        :return: قاموس يحتوي على:
            - text: النص المولد
            - status: success/error
            - metrics: إحصائيات الأداء
        """
        default_params = {
            "max_new_tokens": 300,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "num_return_sequences": 1
        }
        
        params = {**default_params, **(generation_params or {})}
        
        try:
            self.logger.debug(f"📝 معالجة Prompt (أول 100 حرف): {prompt[:100]}...")
            
            start_time = time.time()
            outputs = self.model(prompt, **params)
            latency = time.time() - start_time
            
            result = {
                "text": outputs[0]["generated_text"],
                "status": "success",
                "model": self.model_name,
                "metrics": {
                    "latency_seconds": round(latency, 2),
                    "tokens_generated": len(outputs[0]["generated_text"].split()),
                    "device": self.device
                }
            }
            
            self.logger.info(f"✅ تم توليد {result['metrics']['tokens_generated']} token في {result['metrics']['latency_seconds']} ثانية")
            return result
            
        except Exception as e:
            error_msg = f"❌ فشل التوليد: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return {
                "status": "error",
                "message": error_msg,
                "model": self.model_name
            }

    def __del__(self):
        """تنظيف الذاكرة عند الإنهاء"""
        try:
            if hasattr(self, 'model'):
                del self.model
            if hasattr(self, 'tokenizer'):
                del self.tokenizer
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            self.logger.info("🧹 تم تنظيف الموارد")
        except Exception as e:
            self.logger.warning(f"تحذير أثناء التنظيف: {e}")

# إضافة مفيدة للاستيراد الآمن
def create_hf_integration(model_name: str, hf_token: str, **kwargs) -> Optional[HFIntegration]:
    """دالة مصنع لإنشاء مثيل آمن"""
    try:
        return HFIntegration(model_name, hf_token, **kwargs)
    except Exception as e:
        logging.error(f"فشل إنشاء HFIntegration: {e}")
        return None