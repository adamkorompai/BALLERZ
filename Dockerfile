FROM python:3.9-slim

WORKDIR /usr/src/app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project
COPY . .

# Add the current directory to PYTHONPATH
ENV PYTHONPATH=/usr/src/app 