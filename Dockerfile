# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set default media root inside the container
ENV DJANGO_MEDIA_ROOT=/app/mediafiles

# Set work directory
WORKDIR /app

# Install dependencies
# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run migrations and collect static files
COPY . .
RUN python manage.py migrate --noinput

# Expose the port the app runs on
EXPOSE 8080

# Run the application using Gunicorn
# Adjust workers based on expected load and available resources
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "hf4.wsgi:application"]