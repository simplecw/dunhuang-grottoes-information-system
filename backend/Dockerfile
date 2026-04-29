FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/uploads/images /app/uploads/videos

EXPOSE 5204

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5204"]