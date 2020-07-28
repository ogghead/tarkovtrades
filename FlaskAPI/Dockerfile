FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP flaskapp.py

# gunicorn flaskapp:app

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]