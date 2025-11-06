import os
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv("CANVAS_TOKEN", "")
DOMAIN = os.getenv("CANVAS_DOMAIN", "")
BASE_URL = f"https://{DOMAIN}.instructure.com/api"
