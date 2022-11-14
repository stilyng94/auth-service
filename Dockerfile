FROM python:3.11-slim-bullseye@sha256:f8cc89f5e47347703ec0c2b755464d7db2fa16f255ab860c4b24ba6ef2402020 as base

WORKDIR /usr/app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.2.2 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

RUN apt-get update -y


FROM base as mid

ARG INSTALL_DEV=$INSTALL_DEV

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apt-get install -y --no-install-recommends --no-install-suggests build-essential

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock ./
COPY pyproject.toml ./
COPY ./auth_service ./auth_service

# Allow installing dev dependencies to run tests
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root --no-interaction --no-ansi ; else poetry install --no-root --no-dev --no-interaction --no-ansi ; fi"


FROM base as final

RUN apt-get install -y dumb-init

ENV PATH="/usr/app/.venv/bin:$PATH"

COPY --from=mid /usr/app /usr/app

RUN adduser flask

RUN chown -R flask /usr/app

EXPOSE 5000

USER flask

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/bin/bash", "-c", "flask --app auth_service.app --debug run --host=0.0.0.0"]
