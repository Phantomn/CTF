FROM ubuntu:18.04

EXPOSE 80

RUN apt-get update && apt-get install -y build-essential \
	nginx \
	uwsgi \
	uwsgi-plugin-python \    
    python \
    python-dev\
    python-pip\
    sqlite3

RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y postfix 


ADD ./conf/main.cf /etc/postfix/main.cf
ADD conf/hosts /etc/hosts
RUN chown root:root /etc/hosts

ADD conf/aliases /etc/aliases
RUN chown root:root /etc/aliases


WORKDIR /var/www/html/flask-server

COPY ./app /var/www/html/flask-server/app/
COPY ./conf/default /etc/nginx/sites-available/default
COPY ./conf/uwsgi.ini /etc/uwsgi/apps-available/uwsgi.ini
COPY ./flag /flag

RUN ln -s /etc/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-enabled/


RUN mkdir upload
RUN pip install -r app/requirements.txt


RUN chown -R www-data /var/www/
RUN chown -R root /var/www/html/flask-server/app/


COPY ./start.sh /root/start.sh
RUN chmod +x /root/start.sh
RUN chmod 444 /flag

CMD ["sh", "-c", "/root/start.sh"]
