# 🎬 مشهد سباق السيارات الخارقة الليلي في بلندر (Blender 3D Cinematic Race)

مشروع إنتاج فيلم قصير ثلاثي الأبعاد في بلندر يجسد سباقاً ليلياً بين سيارات خارقة (Bugatti, Porsche, BMW) في شوارع مدينة مظلمة وممطرة مع مؤثرات صوتية سينمائية كاملة.

المشروع مصمم ليعمل **محلياً (Local)** أو سحابياً بالكامل عبر **GitHub Codespaces (عرض الطلاب GitHub Student Developer Pack)** لتوفير موارد الحاسوب الضعيف.

---

## 🚀 كيفية تشغيل المشروع على GitHub Codespaces (عرض الطلاب)

بفضل حزمة الطلاب، يمكنك الاستفادة من خوادم سحابية فائقة القوة (حتى 32GB RAM و16 نوات معالجة) لرندرة الفيلم دون إرهاق حاسوبك الشخصي:

### الخطوة 1: رفع المشروع إلى مستودع GitHub الخاص بك
قم بتشغيل الأوامر التالية من سطر الأوامر (Terminal / PowerShell) في هذا المجلد:

```bash
# 1. تهيئة المستودع (إذا لم تكن مهيأة)
git init -b main

# 2. ربط المستودع الخاص بك على حساب GitHub
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# 3. حفظ ورفع الملفات
git add .
git commit -m "Initial commit with Codespaces and Blender setup"
git push -u origin main
```

*(استبدل `USERNAME` باسم حسابك على GitHub و `REPO_NAME` باسم المستودع الذي أنشأته)*.

---

### الخطوة 2: فتح المشروع في GitHub Codespaces
1. ادخل إلى صفحة المستودع على **GitHub**.
2. اضغط على الزر الأخضر **`<> Code`**.
3. اختر تبويب **`Codespaces`**.
4. اضغط على **`Create codespace on main`**.

> 💡 **ملاحظة:** سيتولى GitHub تلقائياً قراءة ملف `.devcontainer/devcontainer.json`، وتثبيت نظام التشغيل Linux، وتحميل بلندر بكامل مكتبات الرندرة ومكتبات الصوت تلقائياً دون أي تدخل منك!

---

### الخطوة 3: تشغيل الرندرة السحابية
بمجرد أن تفتح نافذة VS Code في المتصفح داخل Codespaces:
1. افتح الـ Terminal (بالضغط على `Ctrl + ~` أو من القائمة).
2. شغّل أمر الرندرة السحابي المباشر:

```bash
bash scripts/render_cloud.sh
```

سيبدأ بلندر بالرندرة واستغلال كامل قوة الأنوية السحابية، وستجد الفيديو النهائي جاهزاً في مجلد `output/final_film.mp4`!

---

### 📥 كيفية تحميل الفيديو النهائي
في شجرة الملفات داخل Codespaces:
* اضغط بزر الفأرة الأيمن (Right Click) على ملف `output/final_film.mp4` واختر **`Download...`** ليتم حفظه مباشرة على جهازك!

---

## 📁 هيكلية المشروع (Project Structure)
* **`.devcontainer/`**: إعدادات بيئة العمل السحابية لـ GitHub Codespaces وتثبيت بلندر.
* **`.github/workflows/`**: تشغيل الرندرة التلقائية عبر GitHub Actions.
* **`scripts/render_cloud.sh`**: سكربت تشغيل الرندرة السحابية باستخدام كل موارد السحابة.
* **`blendswap_api.py`**: عميل تحميل النماذج ثلاثية الأبعاد عبر الـ API.
* **`blender_runner.py`**: مشغل بلندر التلقائي.
* **`cinematic_film/`**: كود بناء المشاهد، تحريك السيارات، وهندسة الصوت.
