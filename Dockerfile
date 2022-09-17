FROM python:3

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY wsgi.py .
COPY data data
COPY classes classes
COPY templates templates
COPY view.py .

ENV FLASK_APP=wsgi.py

CMD  flask run -h 0.0.0.0 -p 80