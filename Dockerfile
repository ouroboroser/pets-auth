FROM python:3.7-buster

WORKDIR /auth

ADD . /auth

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask","run", "--host=0.0.0.0"]