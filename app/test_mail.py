import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_test_email():
    message = MessageSchema(
        subject="Prueba FastAPI-Mail ✅",
        recipients=["diegomoscoso2019@gmail.com"],  # cámbialo por un destino válido
        body="Si ves este mensaje, la configuración SMTP funciona.",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

import asyncio
asyncio.run(send_test_email())