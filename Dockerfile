FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

ENV FLASK_APP simple-python.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
