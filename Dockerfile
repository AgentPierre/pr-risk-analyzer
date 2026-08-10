FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY analyzer/ ./analyzer/
COPY analyze.py .

ENTRYPOINT ["python", "analyze.py"]
