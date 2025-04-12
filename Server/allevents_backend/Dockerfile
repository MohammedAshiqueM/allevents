FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y \
    curl \
    iputils-ping \
    libpq-dev \
    gcc \
    postgresql-client \
    dos2unix \
    libjpeg-dev \
    zlib1g-dev \
    gosu \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh

COPY . /app/

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "allevents_backend.wsgi:application"]