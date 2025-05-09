FROM python:3.14.0b1-alpine
LABEL maintainer="https://github.com/mtpmarin"

WORKDIR /app

RUN apk update && \
    apk add --no-cache \
    ffmpeg \
    libsndfile \
    build-base \
    && rm -rf /var/cache/apk/*

COPY app/ .

CMD ["python", "app.py"]