FROM python:3.14.0b1-alpine
LABEL maintainer="https://github.com/mtpmarin"

ENV TZ=America/Sao_Paulo

WORKDIR /app

RUN apk update && \
    apk add --no-cache \
    ffmpeg \
    libsndfile \
    build-base \
    tzdata \
    && rm -rf /var/cache/apk/*

COPY app/ .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]