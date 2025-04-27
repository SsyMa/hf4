# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV DJANGO_SETTINGS_MODULE=hf4.settings # Change your_project_name
# Set default port Gunicorn will listen on (OpenShift often uses 8080)
ENV PORT=8080
# Set default media root inside the container
ENV DJANGO_MEDIA_ROOT=/app/mediafiles

# Set work directory
WORKDIR /app

# Install dependencies
# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Create directory for media files if it doesn't exist within the image (optional, volume mount is key)
# RUN mkdir -p $DJANGO_MEDIA_ROOT

# Collect static files
# STATIC_ROOT is defined in settings.py relative to BASE_DIR, which is /app here
# Ensure the user running the container has write permissions if needed
# RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE $PORT

# Run the application using Gunicorn
# Adjust workers based on expected load and available resources
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "2", "hf4.wsgi:application"]