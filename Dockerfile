FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN playwright install --with-deps

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
