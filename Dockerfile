FROM python:3-alpine
MAINTAINER mail@martindomke.net
RUN pip install devpi-client requests
COPY opt /opt
