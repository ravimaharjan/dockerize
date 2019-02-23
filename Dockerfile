FROM ubuntu:16.04

MAINTAINER ravi

RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y \
	# git \
	python2.7 \
	# python3-dev \
	# python3-setuptools \
	python-pip \
	nginx \
	supervisor 
	# sqlite3 && \
# RUN pip3 install pip setuptools 
#   rm -rf /var/lib/apt/lists/*

ENV WORKDIR_PATH /home/support
ENV LOG_PATH /var/log

RUN mkdir -p $WORKDIR_PATH
RUN mkdir -p $LOG_PATH

RUN mkdir -p $WORKDIR_PATH/appservice
WORKDIR $WORKDIR_PATH

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code,
# this will cause Docker's caching mechanism to prevent re-installing (all your) 
# dependencies when you made a change a line or two in your app.
COPY requirements.txt $WORKDIR_PATH/appservice
RUN pip install -r $WORKDIR_PATH/appservice/requirements.txt

#COPY rest of the code
COPY . $WORKDIR_PATH/appservice

# RUN chmod +x /home/support/appservice/deploy/app_factory.py

# This is for inter service communication. It is not for the host machine
# EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/home/support/appservice/deploy/run_server.sh"]
CMD ["echo", "Hello world from my first app"]
