- الروبوت: https://t.me/chismegptbpt

[![ar](https://img.shields.io/badge/المتغيرات-ar-red)](https://gg.resisto.rodeo/yo/chatgpTG/src/branch/main/docs/variables/ar.md)

## الأوامر:
- /new - بدء حوار جديد.
- /img - إنشاء صور.
- /retry - إعادة إنشاء آخر رد من الروبوت.
- /chat_mode - تحديد وضع المحادثة.
- /model - عرض نماذج الذكاء الاصطناعي.
- /api - عرض واجهات برمجة التطبيقات.
- /lang - عرض اللغات المتاحة.
- /status - عرض الإعدادات الحالية: النموذج، وضع المحادثة، واجهة برمجة التطبيقات.
- /reset - إعادة تعيين الإعدادات إلى القيم الافتراضية.
- /search - البحث على الإنترنت
- /help – عرض هذه الرسالة مرة أخرى.

## الميزات:
- استدعاء الوظائف! (الوصلات المتصلة مباشرة بـ GPT، نماذج شهر يونيو>).
- قاعدة بيانات JSON محلية.
- قابلية التعديل والتخصيص بشكل كبير.
- اجعل GPT يستخدم الإنترنت باستخدام /search!
- أرسل ملف نصي أو PDF أو عنوان URL وسيتمكن الروبوت من تحليلها!
- أضف بروكسيات عكسية لـ OpenAI ونماذجها المقابلة بقدر ما تريد!
- متعدد اللغات.
- قراءة نص الصور.
- نص الصوت.

# مهم:
- يجب أن تتبع واجهات برمجة التطبيقات المخصصة نفس هيكل OpenAI، أي "https://domain.dom/v1/..."

## الإعداد
1. احصل على مفتاحك من [OpenAI API](https://openai.com/api/)

2. احصل على رمز الروبوت الخاص بك من [@BotFather](https://t.me/BotFather)

3. قم بتعديل `config/api.example.json` لتكوين مفتاح API الخاص بك أو إضافة واجهات برمجة تطبيقات مخصصة

4. أضف رمز Telegram الخاص بك، وقاعدة بيانات Mongo، وقم بتعديل متغيرات أخرى في 'docker-compose.example.yml' وقم بإعادة تسمية `docker-compose.example.yml` إلى `docker-compose.yml`

5. 🔥 قم بالوصول إلى الدليل من خلال الطرفية و**قم بتشغيل**:
    ```bash
    docker-compose up --build
    ```
# سجل النجوم

<a href="https://gg.resisto.rodeo/yo/chatgpTG"><img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=soyelmismo/chatgpTG&type=Date"></a> 

## المراجع
1. المصدر: <a href="https://github.com/karfly/chatgpt_telegram_bot" alt="Karfly">Karfly/chatgpt_telegram_bot</a>