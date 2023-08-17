import json

# Lambda-specific constants
AWS_DEFAULT_REGION_ENV = 'AWS_DEFAULT_REGION'
S3_BUCKET_NAME_ENV = 'S3_BUCKET_NAME'
DEFAULT_REGION = 'us-east-1'
# API response keys
VOLUMES_KEY = 'Volumes'
SNAPSHOTS_KEY = 'Snapshots'
RESPONSE_METADATA_KEY = 'ResponseMetadata'
RESPONSE_STATUS_CODE_KEY = 'HTTPStatusCode'
# API request filters
UNATTACHED_VOLUME_FILTER = [{'Name': 'status', 'Values': ['available']}]
UNENCRYPTED_VOLUME_FILTER = [{'Name': 'encrypted', 'Values': ['false']}]
UNENCRYPTED_SNAPSHOT_FILTER = {'Name': 'encrypted', 'Values': ['false']}


def get_account_own_snapshots_filter(account_id: str):
    return {'Name': 'owner-id', 'Values': [account_id]}


def get_metrics(unattached_volumes, unencrypted_volumes, unencrypted_snapshots) -> str:
    result = {
        'volumes-not-attached': len(unattached_volumes),
        'volumes-not-attached-total-size': sum(vol['Size'] for vol in unattached_volumes),
        'volumes-not-encrypted': len(unencrypted_volumes),
        'volumes-not-encrypted-total-size': sum(vol['Size'] for vol in unencrypted_volumes),
        'snapshots-not-encrypted': len(unencrypted_snapshots),
        'snapshots-not-encrypted-total-size': sum(snap['VolumeSize'] for snap in unencrypted_snapshots),
    }

    return json.dumps(result)
