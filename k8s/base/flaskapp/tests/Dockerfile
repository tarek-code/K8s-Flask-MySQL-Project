FROM python:3.10-slim

WORKDIR /app

# نسخ requirements.txt من المجلد الأب
COPY ../requirements.txt .

# نسخ requirements-tests.txt من نفس المجلد الحالي (tests/)
COPY requirements-tests.txt .

# تثبيت مكتبات الإنتاج
RUN pip install --no-cache-dir -r requirements.txt

# تثبيت مكتبات الاختبار
RUN pip install --no-cache-dir -r requirements-tests.txt

# نسخ باقي ملفات المشروع (من المجلد الأب)
COPY .. .

# الأمر الافتراضي لتشغيل الاختبارات
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-q"]

