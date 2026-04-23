from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("SUPABASE_KEY")
url = os.getenv("SUPABASE_URL")

supabase = create_client(url, key)