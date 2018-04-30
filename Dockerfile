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

# Environment Variables
ENV DB_NAME dainikbhaskar
ENV DB_USER dbcorp
ENV DB_PASSWORD dainik@veris
ENV DB_HOST 13.90.83.192

EXPOSE 8000

CMD NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program uwsgi --ini uwsgi.ini
