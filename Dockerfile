# Use a base Python image
FROM python:3.8-slim

# Set a working directory in the container
WORKDIR /app

# Copy the requirements.txt first to leverage Docker cache when building the image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the necessary files and directories from your project into the container
COPY app/ app/
COPY app_tests/ app_tests/
COPY backups/ backups/
COPY instance/ instance/
COPY run.py .
COPY mydatabase.db .

# Set the command to run your application
CMD ["python", "run.py"]
