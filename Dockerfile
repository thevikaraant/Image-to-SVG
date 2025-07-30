FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PORT=5000

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip     && pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE ${PORT}

CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "app:app"]
