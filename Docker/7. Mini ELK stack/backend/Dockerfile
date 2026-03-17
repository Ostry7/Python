FROM python:3.11-slim

WORKDIR /app
COPY app.py .
RUN pip install flask

RUN mkdir -p /var/log && chmod 777 /var/log

EXPOSE 8001
CMD [ "python", "app.py" ]