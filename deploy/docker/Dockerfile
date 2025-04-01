FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download model file (if not included in repository)
RUN curl -L "https://liveuclac-my.sharepoint.com/:u:/g/personal/zcababr_ucl_ac_uk/EX-K9-PVdlhKkP1IJchp84UB7Qoe5d1vjMKzeriQ2Rwgaw?e=MIE0Tj" -o s2a-q4-hq-fast-en%2Bpl.model

# Expose port
EXPOSE 5001

# Run the application
CMD ["python", "server.py"] 