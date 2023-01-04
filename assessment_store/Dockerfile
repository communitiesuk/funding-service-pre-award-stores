FROM python:3.10-bullseye

WORKDIR /app
# Additional dependency to support Postgres database
RUN apt update && apt -yq install libpq-dev
# install manually to workaround issue in psycopg2-binary 2.9.5
RUN pip3 install psycopg2-binary --no-binary psycopg2-binary
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8080
ENV FLASK_ENV=development

CMD bash -c "flask db upgrade && flask run --host 0.0.0.0 --port 8080"
