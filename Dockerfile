# Use the official Python image as a base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install system dependencies (required for MySQL and Django)
RUN apt-get update && apt-get install -y \
    libmariadb-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the Django application server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
