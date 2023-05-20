FROM python:3.11

WORKDIR /api

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false && poetry install

COPY . .

CMD python ./run.py