import os
from dotenv import load_dotenv

load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "<your_endpoint>")
AZURE_SUBSCRIPTION_KEY = os.getenv("AZURE_SUBSCRIPTION_KEY", "<your_subscription_key>")
