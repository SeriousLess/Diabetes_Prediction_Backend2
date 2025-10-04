from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from app.models.user_model import User
from app.auth.auth_service import get_current_user
import os
import tempfile
import base64
import shutil
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from app.core.mail_config import configuration, mail_from

load_dotenv()

router = APIRouter(prefix="/mail")

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

        # 📂 Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_bytes = base64.b64decode(pdf_base64)
            tmp.write(pdf_bytes)
            tmp_path = tmp.name

        final_path = os.path.join(tempfile.gettempdir(), "resultado-diabetes.pdf")
        shutil.copy(tmp_path, final_path)

        # 📧 Configurar API
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Adjuntar PDF como base64
        with open(final_path, "rb") as f:
            encoded_pdf = base64.b64encode(f.read()).decode()

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email}],
            sender={"email": mail_from, "name": "Sistema Diabetes"},
            subject="📄 Tu PDF adjunto",
            html_content=f"<p>Hola <b>{current_user.username}</b>, aquí tienes tu PDF adjunto ✅</p>",
            attachment=[{
                "content": encoded_pdf,
                "name": "resultado-diabetes.pdf"
            }]
        )

        api_instance.send_transac_email(send_smtp_email)

        # 🗑️ Limpiar archivos temporales
        os.remove(tmp_path)
        os.remove(final_path)

        return JSONResponse(content={"message": f"Correo enviado a {email}"})

    except ApiException as e:
        return JSONResponse(status_code=500, content={"detail": f"Error Brevo API: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Error enviando correo: {str(e)}"})