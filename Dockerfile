# -----------------------------
# Muluki RAG Docker Image
# FastAPI + Streamlit
# -----------------------------

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Hugging Face / Docker port
EXPOSE 7860

# Start FastAPI in background and Streamlit in foreground
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 7860 --server.address 0.0.0.0 --server.headless true"]