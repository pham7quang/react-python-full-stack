# Dockerfile to build an image which can run this backend code
FROM python:3.9.5

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/app/main.py"]
