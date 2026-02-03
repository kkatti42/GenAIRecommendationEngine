from dotenv import load_dotenv
import os

load_dotenv()  # defaults to .env in current dir

LANGSMITH_TRACING = "true"
LANGSMITH_ENDPOINT = "https://api.smith.langchain.com"
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY_RECO")
LANGSMITH_PROJECT = "Reco Agent Project"

# Access your variables
print(f"API Key: {LANGSMITH_API_KEY}")
