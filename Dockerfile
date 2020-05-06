FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y \
        libpq-dev \
        build-essential \
        git \
        sudo \
        unzip zip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt