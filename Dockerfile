FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Imposta il fuso orario (opzionale)
ENV TZ=Europe/Rome

CMD ["python", "multi_spam_free.py"]
