FROM python:3.11-slim

WORKDIR /app

# dépendances système (scikit-learn / shap / psycopg2)
RUN apt-get update && apt-get install -y gcc

# copie du projet
COPY . .

# installation Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# port API
EXPOSE 8000

# lancement FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
