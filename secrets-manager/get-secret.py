# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/

import profile
import sys
import boto3
import base64
from botocore.exceptions import ClientError


def get_secret(s_name) -> None:

    secret_name = s_name
    region_name = "ap-southeast-1"

    # Create a Secrets Manager client
    session = boto3.session.Session(profile_name='datateam')
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage='AWSCURRENT'
        )

        print(get_secret_value_response)
    except Exception as e:
        print(e)
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            print(secret)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            print(decoded_binary_secret)

def list_secret() -> None:
    region_name = "ap-southeast-1"

    # Create a Secrets Manager client
    session = boto3.session.Session(profile_name='datateam')
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )
    response = client.list_secrets()

    print(response['SecretList'])


if __name__ == '__main__':
    secret_name = sys.argv[1]
    get_secret(secret_name)
    # list_secret()