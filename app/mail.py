import smtplib, datetime, config, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import urlparse


def domain_extract(channel):
    parsed = urlparse(channel)
    return parsed.hostname

def check_last_mail(channel):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    domain = domain_extract(channel)
    log_file = f"logs/{domain}.log"

    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')

    if not os.path.exists(log_file):
        with open(log_file, 'w') as file:
            file.write(f"{now_str}")
        return False
    else:
        with open(log_file, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                try:
                    last_time = datetime.datetime.strptime(last_line, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print("Erro ao fazer parsing da data no log.")
                    return True

                if (now - last_time).total_seconds() >= 300:  # mais de 5 minutos
                    with open(log_file, 'w') as file:
                        file.write(f"{now_str}")
                    return False
    return True

def send_mail(channel):
    current_date = datetime.datetime.now()
    subject = f"Silêncio detectado na stream: {channel}"
    html = """\
    <html>
    <body>
        <p>Foi detectado silêncio na stream: <b>{}</b></br></p>
        <p>Horário: <b>{}</b></br></p>
        <p>Verifique o servidor de streaming.</p>
    </body>
    </html>
    """.format(channel, current_date)

    message = MIMEMultipart()
    message["From"] = config.smtp_username
    message["To"] = config.to_addr
    message["Subject"] = subject
    message.attach(MIMEText(html, "html"))

    # Send the email
    if check_last_mail(channel) == True:
        with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
            server.starttls()
            server.login(config.smtp_username)
            server.sendmail(config.smtp_username, config.to_addr, message.as_string())
        return f'Email Enviado com sucesso sobre o canal: {channel}'
    else:
        return 'Email não enviado, já foi enviado um email nos últimos 5 minutos.'


def send_error(channel):
    current_date = datetime.datetime.now()
    subject = f"Falha no monitoramento da stream: {}"
    
    html = """\
    <html>
    <body>
        <p>Não foi possível realizar o monitoramento da stream: <b>{}</b></br></p>
        <p>Horário: <b>{}</b></br></p>
        <p>Verifique o servidor de streaming.</p>
    </body>
    </html>
    """.format(channel, current_date)

    message = MIMEMultipart()
    message["From"] = config.smtp_username
    message["To"] = config.to_addr
    message["Subject"] = subject
    message.attach(MIMEText(html, "html"))

    if check_last_mail(channel) == True:
        with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
            server.ehlo()
            try:
                server.starttls()
            except:
                pass  
            server.sendmail(config.smtp_username, config.to_addr, message.as_string())

        return f'Email enviado com sucesso sobre o canal: {channel}'
    else:
        return 'Email não enviado, já foi enviado um email nos últimos 5 minutos.'