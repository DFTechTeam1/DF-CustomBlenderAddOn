FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry

COPY . /app

RUN chmod +x scripts/setup.sh && sh scripts/setup.sh

EXPOSE 10000

ARG ENV=development

ENV ENV_FILE=env/.env.${ENV}

ENTRYPOINT ["sh", "scripts/run_server.sh"]

CMD ["--development"]
