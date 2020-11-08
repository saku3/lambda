import os
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rds = boto3.client('rds')

EXPORT_TASK_IDENTIFIER = os.environ.get('EXPORT_TASK_IDENTIFIER')
SOURCE_ARN = os.environ.get('SOURCE_ARN')
S3_BUCKETNAME = os.environ.get('S3_BUCKETNAME')
IAM_ROLE_ARN = os.environ.get('IAM_ROLE_ARN')
KMS_KEY_ID = os.environ.get('KMS_KEY_ID')
S3_PREFIX = os.environ.get('S3_PREFIX')


def lambda_handler(event, context):

    logger.info('start:export_snapshot')
    response = rds.start_export_task(
        ExportTaskIdentifier=EXPORT_TASK_IDENTIFIER,
        SourceArn=SOURCE_ARN,
        S3BucketName=S3_BUCKETNAME,
        IamRoleArn=IAM_ROLE_ARN,
        KmsKeyId=KMS_KEY_ID,
        S3Prefix=S3_PREFIX,
        # ExportOnly=[
        #     'string',
        # ]
    )
    logger.info(response)
    logger.info('end:export_snapshots')
