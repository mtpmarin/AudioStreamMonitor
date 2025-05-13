import config
import subprocess
import threading
import logging
import time
from mail import send_mail

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(message)s')
console_handler.setFormatter(formatter)

logger.handlers = []
logger.addHandler(console_handler)

def monitor_stream(stream, detected_problems):
    ffmpeg_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "info",
        "-i", stream,
        "-af", "silencedetect=n=-40dB:d=1",
        "-f", "null", "-"
    ]
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for raw_line in process.stderr:
        line = raw_line.decode("utf-8").strip()

        if "silence_start" in line:
            detected_problems[stream] = 'Silêncio detectado'
            logger.info(f"[{stream}] Silêncio detectado. Início: {line}")
            send_mail(stream)

        elif "silence_end" in line:
            logger.info(f"[{stream}] Silêncio terminou. {line}")

    process_stdout, process_stderr = process.communicate()
    if process.returncode != 0:
        logger.error(f"Erro na execução do ffmpeg para {stream}. Erro: {process_stderr.decode('utf-8')}")

def monitor_multiple_streams(stream_urls):
    threads = []
    detected_problems = {}

    for url in stream_urls:
        logger.info(f"[{url}] Iniciando monitoramento.")
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
    config.stream1,
    config.stream2,
    config.stream3,
    config.stream4
]

monitor_multiple_streams(STREAM_URLS)