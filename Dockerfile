FROM python:3.10-alpine

WORKDIR /app
COPY . /app/
RUN pip3 install -r requirements.txt

CMD python main.py