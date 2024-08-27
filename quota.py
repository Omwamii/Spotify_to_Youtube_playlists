from googleapiclient import discovery
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def check_quota_usage(project_id):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    service = discovery.build('serviceusage', 'v1', credentials=credentials)

    # Define the API call to get the list of services
    request = service.services().list(
        parent=f'projects/{project_id}'
    )
    response = request.execute()

    # Extract and print quota details
    for service_item in response.get('services', []):
        service_name = service_item.get('name')
        print(f"Service: {service_name}")

        # Call to get quota usage for each service
        quota_request = service.services().get(
            name=service_name
        )
        quota_response = quota_request.execute()

        # Print quota details
        quota_info = quota_response.get('quota', {})
        for metric, limits in quota_info.get('metric', {}).items():
            print(f"  Metric: {metric}")
            for limit in limits.get('limit', []):
                print(f"    Limit: {limit['limit']} {limit['unit']}")
                print(f"    Usage: {limit['usage']} {limit['unit']}")


if __name__ == '__main__':
    project_id = 'radiant-snow-418705'
    check_quota_usage(project_id)


class QuotaUsageCalculator():
    """ Calculator for quota usage for the Youtube data API"""
    pass