FROM python:3.10

WORKDIR /app

RUN apt-get update

COPY . .

CMD ["tail", "-f", "/dev/null"]