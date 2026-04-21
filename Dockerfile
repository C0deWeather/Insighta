FROM python:3.12-slim

WORKDIR /insighta

COPY pyproject.toml ./
COPY README.md ./
COPY app ./app

RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
