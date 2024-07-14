# OCR on original art for visually impaired


The goal of this project is to create a tool that can recognize a museum artwork from a photo. 
With this artwork recognition, the museum will be able to provide additional information to 
those who are unable to read the descriptions at the bottom of the artworks (notably the visually impaired).

## Installation
* Docker 27.28.1
* Docker compose v2.28.1
* Python 3.12


## Run

### With docker

* Copy .env_dist to .env and fulfill variables
* Run this commande
```bash
docker compose up
```

### Postgres with docker and FastApi in local
* Copy .env_dist to .env and fulfill variables especially Postgres variables
* Copy .env_dist to .local_en and fulfill variables keep the same values for Postgres variables
* Run commands
```bash
make run_db
```
```bash
make run
```


## Makefile commands summary

Clean database
```bash
make clean
```

Run database :
```bash
make run_db
```

Run FastAPI in local

```bash
make run
```