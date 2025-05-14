# Icecast Local Test Environment

Este ambiente Docker foi criado para realizar testes locais com streaming de áudio usando Icecast.

## Serviços

- **icecast**: Servidor de streaming de áudio acessível na porta `8000`. Senhas básicas estão definidas para facilitar os testes (`admin`, `hackme`, `relay`).
- **ffmpeg**: Responsável por transmitir um arquivo local (`audio.mp3`) para o Icecast automaticamente via script (`ffmpeg-source.sh`).

## Como usar

1. Coloque um arquivo chamado `audio.mp3` no mesmo diretório.

2. Crie ou edite o script `ffmpeg-source.sh` com o comando `ffmpeg` desejado para enviar o áudio para o Icecast.

3. Suba os containers com:

    ```bash
    docker compose up -d
    ````

## Acesso

* Interface do Icecast: [http://localhost:8000](http://localhost:8000)

> Este ambiente é apenas para testes locais e não deve ser usado em produção.
