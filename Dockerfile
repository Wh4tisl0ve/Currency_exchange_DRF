FROM python:3.12-alpine


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN apk update && apk add --no-cache \
    curl \
    python3-dev \
    build-base \
    postgresql-dev \
    && curl -sSL https://install.python-poetry.org | python3 - --preview \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry 
    
RUN adduser -D -s /bin/bash user && chmod 777 /opt /run

WORKDIR /user

RUN mkdir /user/static && chown -R user:user /user && chmod 755 /user

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

COPY --chown=user:user ./src .

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
