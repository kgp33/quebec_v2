# Dockerfile
FROM python:3.9-slim

WORKDIR /quebec_v2

COPY . /quebec_v2

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]