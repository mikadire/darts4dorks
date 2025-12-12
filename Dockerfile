FROM python:3.12-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography

COPY darts4dorks darts4dorks
COPY migrations migrations
COPY app.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP=app.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
