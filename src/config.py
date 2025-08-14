from dotenv import load_dotenv
import os

load_dotenv()
defi_url = os.getenv("DEFI_URL")
db = os.getenv("DB_URL")
