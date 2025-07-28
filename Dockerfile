# Use a small Python image
FROM python:3.9-slim

# Set work directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script into the container
COPY outline_extractor.py .

# Set default command
ENTRYPOINT ["python", "outline_extractor.py"]
