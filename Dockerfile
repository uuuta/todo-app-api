FROM python:3.12 as builder

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock ./

ENV POETRY_VERSION=1.8.5
RUN pip install "poetry==${POETRY_VERSION}"
COPY ["pyproject.toml", "poetry.lock", "./"]
RUN poetry export -f requirements.txt -o requirements.txt

FROM public.ecr.aws/lambda/python:3.12

COPY --from=builder /tmp/requirements.txt requirements.txt
RUN pip install -U pip && \
    pip install -r requirements.txt - target "${LAMBDA_TASK_ROOT}" -U - no-cache-dir

ARG TIMEZONE=Asia/Tokyo
ENV TZ=${TIMEZONE}

COPY ./app ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]
