import os
from dotenv import load_dotenv
from azure.identity import EnvironmentCredential

def get_credential():
    load_dotenv()
    credential = EnvironmentCredential()
    return credential

def get_subscription_id():
    load_dotenv()
    return os.environ.get("AZURE_SUBSCRIPTION_ID")