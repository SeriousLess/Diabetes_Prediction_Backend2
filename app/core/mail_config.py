import os
from dotenv import load_dotenv
import sib_api_v3_sdk

load_dotenv()

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

mail_from = os.getenv("MAIL_FROM")