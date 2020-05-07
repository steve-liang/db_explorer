FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

# Install Ubuntu packages
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    build-essential \
    curl \
    git-core \
    htop \
    pkg-config \
    unzip
# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt