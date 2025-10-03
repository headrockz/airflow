FROM apache/airflow:2.10.3-python3.11

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential gcc python3-dev git libgeos-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && python3 -m pip install --upgrade pip \
  && python3 -m pip install poetry

# RUN chown -R airflow:root /opt/airflow

COPY ./pyproject.toml pyproject.toml

RUN poetry config virtualenvs.in-project false && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

USER airflow
