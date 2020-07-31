FROM python

WORKDIR /restapi

COPY requirements .

RUN pip install -r requirements

COPY . .

ENV FLASK_APP api
ENV FLASK_ENV development

# gunicorn flaskapp:app

ENTRYPOINT flask run --host=0.0.0.0
