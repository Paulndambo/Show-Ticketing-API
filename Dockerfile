# Use an official Python runtime as the base image
FROM python:slim

# Set environment variables (modify as needed)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

RUN apt-get -q update
RUN apt-get -qy install --no-install-recommends wget
RUN wget -nv -O /tmp/wkhtmltox.deb https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb
RUN apt-get -qy install /tmp/wkhtmltox.deb

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Start Gunicorn with 3 workers
CMD ["gunicorn", "ShowTicketing.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]