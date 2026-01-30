FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main_app.py .
COPY app/plant_disease_model.h5 .

ENV MODEL_PATH=/app/plant_disease_model.h5

EXPOSE 8501

RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["streamlit", "run", "main_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
