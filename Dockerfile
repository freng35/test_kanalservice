FROM python:3.8
ENV PYTHONUNBUFFERED 1

COPY . .

WORKDIR .
RUN chmod -R 777 ./docker-entrypoint.sh
RUN pip install -r requirements.txt
