# Monitoramento de Streams de Áudio

Este projeto tem como objetivo monitorar múltiplos streams de áudio e detectar falhas, como períodos de silêncio nas transmissões. Ele utiliza o `ffmpeg` para análise em tempo real e gera logs informando o estado dos streams.

## Funcionalidade

O monitoramento é feito em tempo real em múltiplos streams. A principal detecção é a identificação de silêncio nas transmissões. O programa identifica quando o silêncio começa e termina, e também gera alertas caso o processo de monitoramento termine inesperadamente.

### Requisitos

- Docker

### Bibliotecas Python utilizadas

- `subprocess`: para executar o comando `ffmpeg` e capturar sua saída.
- `threading`: para executar múltiplos monitoramentos de forma simultânea.
- `logging`: para gerar logs durante o processo de monitoramento.
- `time`: para controle de intervalos de verificação e monitoramento contínuo.

### Estrutura do código

1. **Função `monitor_stream(stream, detected_problems)`**:
    - Executa o monitoramento de um único stream utilizando o `ffmpeg`.
    - Detecta a presença de silêncio, gerando logs e armazenando problemas detectados.

2. **Função `monitor_multiple_streams(stream_urls)`**:
    - Inicia múltiplos monitoramentos simultâneos em threads separadas.
    - Realiza verificações a cada 60 segundos para identificar se houve algum problema e gera relatórios a cada intervalo.

3. **Exemplo de Uso**:
   - O script é configurado com uma lista de URLs de streams (`STREAM_URLS`), que são passadas para a função de monitoramento.
   - Para cada URL, uma thread é criada para monitorar o stream.

## Como Usar

1. Crie um arquivo `config.py` com as URLs dos streams, como no exemplo abaixo:

   ```python
   stream1 = 'http://stream-url-1'
   stream2 = 'http://stream-url-2'
   stream3 = 'http://stream-url-3'
   stream4 = 'http://stream-url-4'
    ```

2. Crie a imagem Docker e a inicie:
    ```bash
    docker build . -t image:tag 
    docker run -d image:tag
    ```


## Logs

O script gera logs detalhados no console, indicando:

-   Início do monitoramento de cada stream.
-   Detecção de silêncio.
-   Fim do silêncio.
-   Problemas inesperados (como falhas na execução do `ffmpeg`).

Os logs são exibidos no seguinte formato:

```bash
2025-05-09 12:00:00,000 - [http://stream-url-1] Silêncio detectado. Início: 2025-05-09 12:00:00
2025-05-09 12:01:00,000 - [http://stream-url-2] Silêncio terminou. 2025-05-09 12:01:00
```



Licença
-------

Este projeto é de código aberto e está sob a licença MIT.