FROM python:3.7-slim

ENV HOST=0.0.0.0
ENV PORT=8000

COPY requirements.txt /app/

WORKDIR /app

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install curl && \
    pip3.7 install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --disabled-password --gecos ''  autocomplete

COPY . .

USER autocomplete

HEALTHCHECK --interval=1s --timeout=1s --start-period=2s --retries=3 CMD curl $HOST:$PORT/healthz

CMD ["python", "app.py"]