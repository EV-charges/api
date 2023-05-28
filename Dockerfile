FROM python:3.11-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.4.2
ENV PATH="$POETRY_HOME/bin:$PATH"

FROM python-base AS builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
    && rm -rf /var/lib/apt/lists/*


RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} && \
    chmod a+x /opt/poetry/bin/poetry

WORKDIR API
COPY ./poetry.lock ./pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --only main

COPY . .

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8080"]