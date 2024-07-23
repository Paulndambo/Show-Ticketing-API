# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variables (modify as needed)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory within the container
# Update package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpango1.0-0 \
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install WeasyPrint
RUN apt-get -q update
RUN apt-get -qy install --no-install-recommends wget
RUN apt install weasyprint

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .


# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Start Gunicorn with 3 workers
CMD ["gunicorn", "ShowTicketing.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]