FROM registry.access.redhat.com/ubi8/python-38

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8080

CMD ["python", "app.py"]

