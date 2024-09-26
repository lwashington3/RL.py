FROM python:3.12.5 AS build-package
LABEL authors="Len Washington III"

WORKDIR /usr/src/app

SHELL ["/bin/bash", "-c"]

COPY pyproject.toml ./
COPY MANIFEST.in ./
COPY README.md ./
COPY ./rlpy ./rlpy

RUN pip install --upgrade build
RUN python -m build
RUN chown -R 1000:1000 dist/

FROM python:3.12.5-slim AS base

WORKDIR /usr/src/build

COPY --from=build-package /usr/src/app/dist/rlpy*.whl ./
RUN pip install rlpy*.whl

FROM python:3.12.5-slim AS prod
ENV TZ="America/Chicago"

WORKDIR /usr/src/app

RUN apt update && apt upgrade -y && apt autoremove -y
# region Configures the timezone
RUN apt install -yq tzdata && \
    ln -fs "/usr/share/zoneinfo/$TZ" /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
# endregion

ENTRYPOINT ["python3", "-m"]

COPY --from=base /usr/local/bin/rlpy /usr/local/bin/rlpy
COPY --from=base /usr/local/bin/playwright /usr/local/bin/playwright
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

RUN playwright install-deps && playwright install firefox
