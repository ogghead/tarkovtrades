FROM python

WORKDIR /restapi

COPY requirements .

RUN pip install -r requirements

COPY . .

ENV FLASK_APP restapi

# gunicorn flaskapp:app

# ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT flask run --host=0.0.0.0
