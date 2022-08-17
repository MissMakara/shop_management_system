FROM python:3.9

WORKDIR /app
ADD . /app

ENV TZ=Africa/Nairobi
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip3 install -r /app/requirements.txt

CMD [ "uwsgi", "uwsgi.ini" ]
