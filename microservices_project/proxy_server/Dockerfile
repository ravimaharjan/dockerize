FROM nginx:latest

#RUN apt-get update

ENV WORKDIR_PATH /home/support

RUN mkdir -p $WORKDIR_PATH


RUN mkdir -p $WORKDIR_PATH/lpsm
WORKDIR $WORKDIR_PATH

ADD ./static /usr/share/nginx/html

ADD nginx.conf /etc/nginx/conf.d/default.conf

ENV NGINX_PORT 80

EXPOSE 80

CMD /bin/bash -c "nginx -g 'daemon off;'"