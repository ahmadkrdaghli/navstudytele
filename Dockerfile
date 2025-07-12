FROM python:3.11-slim

WORKDIR /app

# نسخ ملفات المشروع (main.py + ملف المتطلبات)
COPY main.py .
COPY requirements.txt .

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
