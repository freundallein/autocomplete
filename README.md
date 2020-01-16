# autocomplete
[![Build Status](https://travis-ci.org/freundallein/autocomplete.svg?branch=master)](https://travis-ci.org/freundallein/autocomplete)

Simple autocomplete service


## Configuration
Application supports configuration via environment variables:
```
HOST=0.0.0.0
PORT=8000
TOP=5  # amount of words in server response
# persistent storage 
DB_HOST=mongo
DB_PORT=27017
DB_USER=autocomplete
DB_PASSWORD=autocomplete
```
## Installation
### With docker  
```
$> docker pull freundallein/autocomplete
```
### With source
```
$> git clone git@github.com:freundallein/autocomplete.git
$> cd autocomplete
$> pip install -r requirements.txt
```

## Usage
Docker-compose
```
version: "3.5"

networks:
  network:
    name: example-network
    driver: bridge

services:
  autocomplete:
    image: freundallein/autocomplete:latest
    container_name: autocomplete
    restart: always
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TOP=5
      - DB_HOST=mongo
      - DB_PORT=27017
      - DB_USER=autocomplete
      - DB_PASSWORD=autocomplete
    depends_on: 
      - mongo
    networks: 
      - network
    ports:
      - 8000:8000

  mongo:
    image: mongo
    container_name: mongodb
    restart: always
    environment:
      - MONGO_INITDB_ROOT_USERNAME=autocomplete
      - MONGO_INITDB_ROOT_PASSWORD=autocomplete
    command: --wiredTigerCacheSizeGB 1.5
    volumes:
      -  ./localdb:/data/db
    networks: 
      - network
```
After start you have service with loaded to persistent storage corpus of english words with some frequency.
You can make http requests: 
```
GET 0.0.0.0:8000/?prefix=a&top=3
```
will return  
`{"words": [{"word": "a", "frequency": 155432}, {"word": "are", "frequency": 49961}, {"word": "and", "frequency": 41182}], "len": 3}`

Also you can add new words or update frequency of existing with 
```
curl -X POST -d '{"word":"Example"}' -H "Content-Type: application/json"  0.0.0.0:8000
```

## Metrics
Prometheus metrics are available on `/metrics`.


## Healthcheck
Service healthcheck is avaliable on `/healthz`.  
Return `200` if service ready esle `500`.

Good luck.
