import smtplib, datetime, config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(channel):
    current_date = datetime.datetime.now()
    subject = f"Silêncio detectado na stream: {channel}"
    html = """\
    <html>
    <body>
        <p>Foi detectado silêncio na stream: <b>f{channel}</b></br></p>
        <p>Horário: <b>{current_date}</b></br></p>
        <p>Verifique o servidor de streaming.</p>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message["From"] = config.smtp_username
    message["To"] = config.to_addr
    message["Subject"] = subject
    message.attach(MIMEText(html, "html"))

    # Send the email
    with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
        server.starttls()
        server.login(config.smtp_username)
        server.sendmail(config.smtp_username, config.to_addr, message.as_string())

    return 'Email Enviado com sucesso sobre o canal: f{channel}'


def send_error(channel):
    current_date = datetime.datetime.now()
    subject = f"Falha no monitoramento da stream: {channel}"
    html = """\
    <html>
    <body>
        <p>Não foi possível realizar o monitoramento da stream: <b>f{channel}</b></br></p>
        <p>Horário: <b>{current_date}</b></br></p>
        <p>Verifique o servidor de streaming.</p>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message["From"] = config.smtp_username
    message["To"] = config.to_addr
    message["Subject"] = subject
    message.attach(MIMEText(html, "html"))

    # Send the email
    with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
        server.starttls()
        server.login(config.smtp_username)
        server.sendmail(config.smtp_username, config.to_addr, message.as_string())

    return 'Email Enviado com sucesso sobre o canal: f{channel}'