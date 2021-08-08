FROM python:3.9-slim

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

WORKDIR /app
COPY . .

ENTRYPOINT ["./run_gunicorn.sh"]

