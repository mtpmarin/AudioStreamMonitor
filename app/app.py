import config
import subprocess, threading, logging, time, os
from mail import send_mail, send_error
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


## Parameters to connecto to InfluxDB
influxurl= 'http://'+ os.environ['INFLUXDB_HOST']  +':8086'
influxtoken= os.environ['INFLUXDB_TOKEN']
influxorg = os.environ['INFLUXDB_ORG']
influxbucket = os.environ['INFLUXDB_BUCKET']

client = InfluxDBClient(url=influxurl, token=influxtoken, org=influxorg)
write_api = client.write_api(write_options=SYNCHRONOUS)

def log_to_influx(stream, event_type, message):
    point = (
        Point("stream_event")
        .tag("stream", stream)
        .tag("event", event_type)
        .field("message", message)
    )
    write_api.write(bucket=influxbucket, org=influxorg, record=point)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(message)s')
console_handler.setFormatter(formatter)

logger.handlers = []
logger.addHandler(console_handler)

def monitor_stream(stream, detected_problems, max_retries=5, retry_delay=10):
    retries = 0

    while retries <= max_retries:
        ffmpeg_cmd = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "info",
            "-i", stream,
            "-af", "silencedetect=n=-40dB:d=1",
            "-f", "null", "-"
        ]
        logger.info(f"[{stream}] Iniciando monitoramento (tentativa {retries + 1}/{max_retries + 1})")
        
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            for raw_line in process.stderr:
                line = raw_line.decode("utf-8").strip()

                if "silence_start" in line:
                    detected_problems[stream] = 'Silêncio detectado'
                    logger.info(f"[{stream}] Silêncio detectado. Início: {line}")
                    send_mail(stream)
                    log_to_influx(stream, "silence_start", line)

                elif "silence_end" in line:
                    logger.info(f"[{stream}] Silêncio terminou. {line}")
                    log_to_influx(stream, "silence_end", line)


            # Aguarda o processo encerrar
            process_stdout, process_stderr = process.communicate()

            if process.returncode != 0:
                logger.warning(f"[{stream}] ffmpeg terminou com erro. Tentando reconectar em {retry_delay} segundos...")
                log_to_influx(stream, "connection_failure", f"[{stream}] ffmpeg terminou com erro.")
                retries += 1
                time.sleep(retry_delay)
            else:
                break

        except Exception as e:
            logger.error(f"[{stream}] Erro inesperado durante monitoramento: {e}")
            log_to_influx(stream, "unexpected_error", f"[{stream}] Erro inesperado durante monitoramento.")
            retries += 1
            time.sleep(retry_delay)

    if retries > max_retries:
        logger.error(f"[{stream}] Falha permanente após {max_retries + 1} tentativas. Stream indisponível.")
        detected_problems[stream] = 'Erro de conexão permanente'
        send_error(stream)
        log_to_influx(stream, "connection_failure", "Falha após múltiplas tentativas.")


def monitor_multiple_streams(stream_urls):
    threads = []
    detected_problems = {}

    for url in stream_urls:
        thread = threading.Thread(target=monitor_stream, args=(url, detected_problems))
        threads.append(thread)
        thread.start()

    last_report_time = time.time()

    while True:
        time.sleep(60)
        if detected_problems:
            logger.info("Problema detectado, verificando novamente em 1 minuto.")
        else:
            logger.info("Nenhum problema detectado no último 1 minuto.")

        detected_problems.clear()

        for thread in threads:
            if not thread.is_alive():
                logger.warning("Um dos monitoramentos foi encerrado inesperadamente.")
                

STREAM_URLS = [
    config.fmandroid,
    config.fmios,
    config.parceiros,
    config.teste
]

monitor_multiple_streams(STREAM_URLS)