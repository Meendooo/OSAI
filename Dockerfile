FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN mkdir -p /app/data/pdfs /app/data/processed /app/data/analysis


CMD ["python", "src/tei_analyzer.py"]
