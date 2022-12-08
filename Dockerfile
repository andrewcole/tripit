FROM docker.io/library/python:3.11.1

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    XDG_CONFIG_HOME=/config

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r ./requirements.txt

COPY . /usr/src/app
RUN pip3 install --no-cache-dir .

ENTRYPOINT ["/usr/local/bin/tripit-api-to-json"]