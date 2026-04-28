FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

ENV ENVIRONMENT=hf

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
