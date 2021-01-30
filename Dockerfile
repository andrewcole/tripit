FROM docker.io/library/python:3.9.1 AS importer

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    XDG_CONFIG_HOME=/config

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt

ADD ./tripit.json /usr/src/app/tripit.json
RUN cat tripit.json | tripit-json-to-sqlite -

FROM docker.io/datasetteproject/datasette:0.54
COPY --from=importer /usr/src/app/tripit.db /mnt/tripit.db
COPY ./metadata.json /mnt/metadata.json
CMD ["datasette", "-p", "80", "-h", "0.0.0.0", "--metadata", "/mnt/metadata.json", "/mnt/tripit.db"]

ARG VCS_REF
ARG VERSION
ARG BUILD_DATE
LABEL maintainer="Andrew Cole <andrew.cole@illallangi.com>" \
      org.label-schema.build-date=${BUILD_DATE} \
      org.label-schema.description="Tripit Datasette container" \
      org.label-schema.name="tripit-datasette" \
      org.label-schema.schema-version="1.0" \
      org.label-schema.url="http://github.com/andrewcole/tripit" \
      org.label-schema.usage="https://github.com/andrewcole/tripit/blob/master/README.md" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/andrewcole/tripit" \
      org.label-schema.vendor="Andrew Cole" \
      org.label-schema.version=$VERSION
