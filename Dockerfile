FROM python:3.13.1 as base

ENV PYTHONPATH=/opt/darmaai
ENV PYTHONUNBUFFERED=1
ENV PYTHONBREAKPOINT=ipdb.set_trace
RUN addgroup darmaai && useradd -u 1000 darmaai -g darmaai -G tty

COPY --chown=darmaai:darmaai ./requirements /opt/requirements

RUN set -ex && \
  apt-get update --yes && \
  apt-get upgrade --yes && \
  apt-get install --no-install-recommends --yes curl sqlite3 libsqlite3-dev redis-tools && \
  pip install --no-cache-dir --disable-pip-version-check pip-tools && \
  pip-sync /opt/requirements/base.txt --pip-args '--no-cache-dir --no-deps --disable-pip-version-check' && \
  rm -rf /var/lib/apt/lists/*

FROM base as full

ARG APP_ENV=production
ENV APP_ENV=$APP_ENV

RUN if [ $APP_ENV = "production" ]; then \
        pip-sync /opt/requirements/base.txt --pip-args '--no-cache-dir --no-deps --disable-pip-version-check'; \
    else \
        pip-sync /opt/requirements/base.txt /opt/requirements/test.txt --pip-args '--no-cache-dir --no-deps --disable-pip-version-check'; \
    fi

RUN mkdir -m 775 /home/darmaai && \
  chown darmaai:darmaai /home/darmaai/

COPY --chown=darmaai:darmaai . /opt/darmaai/

WORKDIR /opt/darmaai/src

USER darmaai

EXPOSE 8000
