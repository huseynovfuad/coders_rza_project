FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt