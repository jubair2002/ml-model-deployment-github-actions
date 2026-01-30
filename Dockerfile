FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main_app.py app/plant_disease_model.h5 ./

ENV MODEL_PATH=/app/plant_disease_model.h5
EXPOSE 8501

CMD ["streamlit", "run", "main_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
