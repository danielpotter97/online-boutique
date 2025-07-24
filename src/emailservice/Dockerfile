FROM python:3.12.8-slim

WORKDIR /email_server

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8080
ENV PYTHONUNBUFFERED=1
ENTRYPOINT [ "python", "email_server.py" ]
