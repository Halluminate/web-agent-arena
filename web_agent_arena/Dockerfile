FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p static templates

# Copy the rest of the application
COPY . .

# Make startup script executable
RUN chmod +x startup.sh

# Expose the port
EXPOSE 8000

# Run the application
CMD ["./startup.sh"]
