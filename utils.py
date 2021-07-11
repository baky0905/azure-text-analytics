from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os

load_dotenv()


def authenticate_client():
    ta_credential = AzureKeyCredential(os.getenv("KEY"))
    text_analytics_client = TextAnalyticsClient(
        endpoint=os.getenv('ENDPOINT'),
        credential=ta_credential)
    return text_analytics_client
