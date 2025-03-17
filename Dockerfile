FROM python:3.12

ENV PYTHONBUFFERED=1

# Путь с которого все выполняется внутри контейнера, папка автоматичски будет создвна, если ее нет
WORKDIR app/

RUN pip install -U pip "poetry==1.8.4"
RUN poetry config virtualenvs.create false --local

# Возьми 2 poetry файла локально и скопируй их в контейнер, по пути ./ (WORKDIR)
COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY config.example.toml ./
# Возьми папку app с текущего локального уровня (BaseFastAPI) и скопируй ее в контейнер, где . это
# WORKDIR в Dockerfile от куда все скрипты запускаются и перенеси ее с этого уровня . в папку app/
COPY app/ ./app/

ENV PYTHONPATH=/app

#запуск идет с WORKDIR/app/main.py
CMD ["python", "app/main.py"]