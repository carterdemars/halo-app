# Use official lightweight Python image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Start Gunicorn server (Flask app)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
