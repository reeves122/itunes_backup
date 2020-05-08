FROM python:3.7-alpine

ADD itunes_backup.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./itunes_backup.py" ]