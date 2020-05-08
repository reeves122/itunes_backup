FROM python:3.7-alpine

ADD itunes_backup.py /

CMD [ "python", "./itunes_backup.py" ]