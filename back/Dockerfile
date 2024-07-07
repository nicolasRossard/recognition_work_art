FROM python:3.12.2-bullseye
LABEL authors="nicolas.rossard"

ADD . /code/fast

WORKDIR /code/fast

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "--workers", "1", "--host", "0.0.0.0", "--port", "3000", "--reload", "app.main:app"]
