from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.models.user_model import User
from app.auth.auth_service import get_current_user
import os
import tempfile
import base64
import shutil
from dotenv import load_dotenv

# 👇 Cargar variables de entorno
load_dotenv()

router = APIRouter(prefix="/mail")

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True,
)

@router.post("/send-pdf")
async def send_pdf(
    data: dict = Body(...), 
    current_user: User = Depends(get_current_user)
):
    try:
        email = data.get("email")
        pdf_base64 = data.get("pdf_content")

        if not email or not pdf_base64:
            return JSONResponse(status_code=400, content={"detail": "Faltan datos (email o pdf_content)"})

        # 📂 Crear archivo temporal con nombre fijo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_bytes = base64.b64decode(pdf_base64)
            tmp.write(pdf_bytes)
            tmp_path = tmp.name

        # 🔹 Copiar a un archivo con nombre más bonito
        final_path = os.path.join(tempfile.gettempdir(), "resultado-diabetes.pdf")
        shutil.copy(tmp_path, final_path)

        # 📧 Preparar mensaje
        message = MessageSchema(
            subject="📄 Tu PDF adjunto",
            recipients=[email],
            body=f"Hola {current_user.username}, aquí tienes tu PDF adjunto ✅",
            attachments=[final_path],  # 👉 adjuntamos el archivo con nombre fijo
            subtype="plain"
        )

        fm = FastMail(conf)
        await fm.send_message(message)

        # 🗑️ Limpiar archivos temporales
        os.remove(tmp_path)
        os.remove(final_path)

        return JSONResponse(content={"message": f"Correo enviado a {email}"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Error enviando correo: {str(e)}"})