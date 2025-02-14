FROM python:3.11-slim

WORKDIR /exchange_parser

#RUN apt-get update && apt-get install -y \
#    build-essential \
#    libpq-dev \
#    curl \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /exchange_parser/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

#COPY . /exchange_parser/
# TODO Раскомментить при деплое, убрать том из докер композ

ENV PYTHONPATH=/exchange_parser

#ENTRYPOINT ["sh", "-c", "alembic -c /exchange_parser/database/alembic.ini upgrade head && python main.py"]
ENTRYPOINT ["/bin/sh", "-c", "python main.py"]
