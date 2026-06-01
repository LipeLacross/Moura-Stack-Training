import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from pathlib import Path
from datetime import datetime
from typing import Optional


class EmailReporter:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_report(
        self,
        to_emails: list[str],
        subject: str,
        body_html: str,
        attachments: Optional[list[Path]] = None,
    ):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.username
        message["To"] = ", ".join(to_emails)

        part_html = MIMEText(body_html, "html")
        message.attach(part_html)

        if attachments:
            for filepath in attachments:
                with open(filepath, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f'attachment; filename="{filepath.name}"',
                    )
                    message.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, to_emails, message.as_string())

    def build_kpi_html(self, kpis: dict) -> str:
        cards = "".join(
            f'<div style="display:inline-block;padding:16px;margin:8px;'
            f'background:#f0f4ff;border-radius:8px;text-align:center;'
            f'min-width:150px">'
            f'<h3 style="margin:0;color:#1a56db">{value}</h3>'
            f'<p style="margin:4px 0 0;color:#374151;font-size:14px">{label}</p>'
            f"</div>"
            for label, value in kpis.items()
        )
        return f"""
        <html>
        <head><meta charset="utf-8"></head>
        <body style="font-family:Arial,sans-serif;padding:24px">
            <h2 style="color:#1a56db">Relatório Automático - Moura TI</h2>
            <p>Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <div style="margin:24px 0">{cards}</div>
            <hr>
            <p style="color:#6b7280;font-size:12px">
                Este é um relatório automático do sistema de monitoramento.
            </p>
        </body>
        </html>
        """
