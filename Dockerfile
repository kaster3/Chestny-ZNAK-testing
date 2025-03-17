FROM python:3.12

ENV PYTHONBUFFERED=1

WORKDIR app/

RUN pip install -U pip "poetry==1.8.4"
RUN poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY config.example.toml ./

COPY app/ ./app/

ENV PYTHONPATH=/app

CMD ["tail", "-f", "/dev/null"]