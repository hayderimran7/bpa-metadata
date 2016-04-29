FROM muccg/bpametadata:next_release
MAINTAINER https://github.com/muccg/bpa-metadata

ENV PIP_OPTS="--no-cache-dir"

USER root

COPY requirements /app/requirements
WORKDIR /app

RUN /env/bin/pip freeze
RUN /env/bin/pip ${PIP_OPTS} uninstall -y bpam
RUN /env/bin/pip ${PIP_OPTS} install --upgrade -r requirements/dev-requirements.txt
RUN /env/bin/pip ${PIP_OPTS} install --upgrade -r requirements/test-requirements.txt

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY . /app
RUN /env/bin/pip ${PIP_OPTS} install -e bpam

EXPOSE 8000 9000 9001 9100 9101
VOLUME ["/app", "/data"]

ENV HOME /data
WORKDIR /data

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["runserver"]
