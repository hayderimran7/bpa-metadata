#
FROM muccg/python-base:ubuntu14.04-2.7
MAINTAINER ccg <ccgdevops@googlegroups.com>

ENV DEBIAN_FRONTEND noninteractive

# Project specific deps
RUN apt-get update && apt-get install -y \
  git \
  libpcre3 \
  libpcre3-dev \
  libgeos-c1 \
  libpq-dev \
  libssl-dev \
  libxml2-dev \
  libxslt1-dev \
  python-tk \
  postgresql-client \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN env --unset=DEBIAN_FRONTEND

# Deps for tests
RUN pip install \
  lettuce \
  lettuce_webdriver \
  nose \
  selenium

# Install dependencies only (not the app itself) to use the build cache more efficiently
# This will be redone only if setup.py changes
# INSTALL_ONLY_DEPENDENCIES stops the app installing inside setup.py (pip --deps-only ??)
COPY bpam/setup.py /app/bpam/setup.py
WORKDIR /app/bpam
RUN INSTALL_ONLY_DEPENDENCIES=True pip install --process-dependency-links .

# Copy code and install the app
COPY . /app
RUN pip install --process-dependency-links --no-deps -e .

# now that we have installed everything globally purge /app
# /app gets added as a volume at run time
WORKDIR /app
RUN rm -rf ..?* .[!.]* *

EXPOSE 8000 9000 9001 9100 9101
VOLUME ["/app", "/data"]

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Drop privileges, set home for ccg-user
USER ccg-user
ENV HOME /data
WORKDIR /data

ENV APP_RELEASE BLEEDING_EDGE
ENV PYTHONUNBUFFERED=1
# entrypoint shell script that by default starts runserver
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["runserver"]
