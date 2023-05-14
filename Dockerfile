FROM python:3.9-alpine

COPY . /app
WORKDIR /app
RUN chmod 777 /app/startServices.sh
RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["/app/startServices.sh"]
