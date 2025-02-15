# Use Python as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8000

# Run migrations and start the server
CMD ["/bin/bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
