import logging
import os

import boto3

from constants import VOLUMES_KEY, SNAPSHOTS_KEY, RESPONSE_METADATA_KEY, RESPONSE_STATUS_CODE_KEY, \
    UNATTACHED_VOLUME_FILTER, UNENCRYPTED_FILTER

log = logging.Logger('')


def lambda_handler(event, context):
    try:
        ec2_client = get_ec2_client()
        unencrypted_volumes = get_unencrypted_volumes(ec2_client)
        log.debug(f'Got unencrypted volumes: {unencrypted_volumes}')
    except Exception as e:
        log.error(f'Something went wrong: {repr(e)}')


def get_ec2_client() -> boto3.client:
    lambda_region_env_var = 'AWS_DEFAULT_REGION'
    default_region = 'us-east-1'
    region = os.getenv(lambda_region_env_var, default_region)
    return boto3.client('ec2', region)


def get_unattached_volumes(ec2: boto3.client):
    response = ec2.describe_volumes(Filters=UNATTACHED_VOLUME_FILTER)
    validate_client_response(response=response, required_key=VOLUMES_KEY)
    validate_client_response(response)
    return response


def get_unencrypted_volumes(ec2: boto3.client):
    response = ec2.describe_volumes(Filters=UNENCRYPTED_FILTER)
    validate_client_response(response=response, required_key=VOLUMES_KEY)
    return response


def get_unencrypted_snapshots(ec2: boto3.client):
    response = ec2.describe_snapshots(Filters=UNENCRYPTED_FILTER)
    validate_client_response(response=response, required_key=SNAPSHOTS_KEY)
    return response


def validate_client_response(response, required_key=None):
    http_ok_status = 200
    if RESPONSE_METADATA_KEY in response and RESPONSE_STATUS_CODE_KEY in response[RESPONSE_METADATA_KEY]:
        if response[RESPONSE_METADATA_KEY][RESPONSE_STATUS_CODE_KEY] == http_ok_status:
            pass
    if not required_key or (required_key and required_key in response):
        return
    raise Exception(f'Failed validating client response: {str(response)}')


# For local development
if __name__ == '__main__':
    lambda_handler(None, None)
