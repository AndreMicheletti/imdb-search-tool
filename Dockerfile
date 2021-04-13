FROM python:3.6.1-alpine

WORKDIR /app

RUN pip install --upgrade pip
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ENV CACHE_TYPE=memory

ADD . /app
EXPOSE 5000

CMD ["python","app.py"]