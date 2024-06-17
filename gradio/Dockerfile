FROM python:3.11-bullseye

WORKDIR /code/gradio

COPY . /code/gradio

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "app/main.py"]
