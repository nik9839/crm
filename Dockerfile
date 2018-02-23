FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y \
    python3-dev \
    python-psycopg2 \
    libpq-dev \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements /usr/src/app/requirements
RUN pip install -r requirements/requirements.txt

COPY client_secret.json /usr/src/app/
COPY . /usr/src/app

EXPOSE 8000

CMD ./manage.py runserver 0.0.0.0:8000 

