import logging
import os
import sys
from datetime import datetime

import boto3

from constants import (VOLUMES_KEY, SNAPSHOTS_KEY, RESPONSE_METADATA_KEY, RESPONSE_STATUS_CODE_KEY,
                       UNATTACHED_VOLUME_FILTER, UNENCRYPTED_VOLUME_FILTER, UNENCRYPTED_SNAPSHOT_FILTER,
                       AWS_DEFAULT_REGION_ENV, DEFAULT_REGION, S3_BUCKET_NAME_ENV, get_account_own_snapshots_filter,
                       get_metrics)

_logger = logging.getLogger()
_streamHandler = logging.StreamHandler(sys.stdout)
_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_streamHandler.setFormatter(_formatter)
_logger.setLevel(logging.WARN)
_logger.addHandler(_streamHandler)
log = _logger


def lambda_handler(event, context):
    try:
        ec2 = get_boto_client('ec2')

        unencrypted_volumes = get_unencrypted_volumes(ec2)
        unattached_volumes = get_unattached_volumes(ec2)
        unencrypted_snapshots = get_unencrypted_snapshots(ec2)

        ebs_metrics = get_metrics(unencrypted_volumes=unencrypted_volumes, unattached_volumes=unattached_volumes,
                                  unencrypted_snapshots=unencrypted_snapshots)
        store_results(ebs_metrics)
    except Exception as e:
        log.error(f'Something went wrong: {repr(e)}')


def get_boto_client(service):
    region = os.getenv(AWS_DEFAULT_REGION_ENV, DEFAULT_REGION)
    return boto3.client(service, region)


def get_account_id():
    # To avoid storing account id in the code
    sts = get_boto_client('sts')
    return sts.get_caller_identity()['Account']


def validate_client_response(response, required_key=None):
    http_ok_status = 200
    if RESPONSE_METADATA_KEY in response and RESPONSE_STATUS_CODE_KEY in response[RESPONSE_METADATA_KEY]:
        if response[RESPONSE_METADATA_KEY][RESPONSE_STATUS_CODE_KEY] == http_ok_status:
            pass
    if not required_key or (required_key and required_key in response):
        return
    raise Exception(f'Failed validating client response: {str(response)}')


def get_unattached_volumes(ec2: boto3.client):
    response = ec2.describe_volumes(Filters=UNATTACHED_VOLUME_FILTER)
    validate_client_response(response=response, required_key=VOLUMES_KEY)
    return response[VOLUMES_KEY]


def get_unencrypted_volumes(ec2: boto3.client):
    response = ec2.describe_volumes(Filters=UNENCRYPTED_VOLUME_FILTER)
    validate_client_response(response=response, required_key=VOLUMES_KEY)
    return response[VOLUMES_KEY]


def get_unencrypted_snapshots(ec2: boto3.client):
    account_id = get_account_id()
    current_account_snapshot_filter = get_account_own_snapshots_filter(account_id)
    response = ec2.describe_snapshots(Filters=[current_account_snapshot_filter, UNENCRYPTED_SNAPSHOT_FILTER])
    validate_client_response(response=response, required_key=SNAPSHOTS_KEY)
    return response[SNAPSHOTS_KEY]


def store_results(results: str):
    bucket_name = os.getenv(S3_BUCKET_NAME_ENV)
    log.info(f'Uploading  results into bucket {bucket_name}')

    s3 = get_boto_client('s3')
    now = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    object_key = f'ebs-metrics-{now}.json'
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=results)


if __name__ == '__main__':
    # Local development entrypoint
    lambda_handler(None, None)
