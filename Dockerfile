FROM python:3.12-slim
RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml  ./
RUN poetry lock
RUN poetry install --no-root

ARG SERVICE
ENV SERVICE = ${SERVICE}

COPY . .
CMD ["uvicorn", "fastapi_client.api.main_fast:app", "--host", "0.0.0.0", "--port", "6000"]