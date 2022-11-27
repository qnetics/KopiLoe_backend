# setting nginx for deploy backend service
FROM nginx:1.22.1

COPY nginx.conf /etc/nginx/conf.d/default.conf


# setting backend service deployment
FROM python:3.9

WORKDIR /opt/kopiloe_backend_service 

COPY . .
EXPOSE 80

RUN pip3 install -r requirements.txt

RUN python3 manage.py migrate --run-syncdb
RUN python3 manage.py makemigrations
