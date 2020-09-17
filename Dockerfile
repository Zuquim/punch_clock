FROM python:3.8-alpine
LABEL fun.app.name="PunchClock" \
      fun.app.version="0.1.0"
WORKDIR /app
COPY . ./
ENV ENV production
ENV FLASK_APP punch_clock.py
ENV FLASK_ENV $ENV
RUN apk update && apk add --no-cache -U tzdata && \
    ln /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    mkdir /var/db && mkdir /var/log/app && \
    pip install -U pip setuptools && \
    pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["gunicorn", "--pid=/var/run/punch_clock.pid", "--workers=2", "--threads=4", "--bind=0.0.0.0:80", "--log-level=info", "--access-logfile=/var/log/api/access.log", "--error-logfile=/var/log/api/error.log", "punch_clock:app"]
