FROM docker.io/library/python:3.10.5

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    XDG_CONFIG_HOME=/config

WORKDIR /usr/src/app

ADD requirements.txt .
RUN pip3 install -r ./requirements.txt

ADD . /usr/src/app
RUN pip3 install .

ENTRYPOINT ["/usr/local/bin/tripit-api-to-json"]