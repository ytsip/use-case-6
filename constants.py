# API response keys
VOLUMES_KEY = 'Volumes'
SNAPSHOTS_KEY = 'Snapshots'
RESPONSE_METADATA_KEY = 'ResponseMetadata'
RESPONSE_STATUS_CODE_KEY = 'HTTPStatusCode'
# API request filters
UNATTACHED_VOLUME_FILTER = [{'Name': 'status', 'Values': ['Available']}]
UNENCRYPTED_FILTER = [{'Name': 'encrypted', 'Values': ['false']}]
