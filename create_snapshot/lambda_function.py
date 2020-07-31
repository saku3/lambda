import os
import json
import boto3
import logging
import time
from datetime import datetime, timedelta, tzinfo

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rds = boto3.client('rds')


def lambda_handler(event, context):
    instance_id = os.environ.get('INSTANCE_ID')
    delete_retention_period = int(os.environ.get('DELETE_RETENTION_PERIOD'))

    logger.info('start:create_snapshots')
    create_snapshot(instance_id)
    logger.info('end:create_snapshots')

    logger.info('start:delete_snapshots')
    delete_snapshots(instance_id, delete_retention_period)
    logger.info('end:delete_snapshots')


def delete_snapshots(instance_id, delete_retention_period):
    snapshots = rds.describe_db_snapshots(
        DBInstanceIdentifier=instance_id, SnapshotType='manual')

    snapshot_list = list(
        filter(lambda x: x['Status'] == 'available', snapshots['DBSnapshots']))
    snapshot_list.sort(key=lambda x: x['SnapshotCreateTime'], reverse=True)

    for snapshot in snapshot_list[delete_retention_period:]:
        logger.info(f"deleted:{snapshot['DBSnapshotIdentifier']}")
        rds.delete_db_snapshot(
            DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier'])


def create_snapshot(instance_id):
    new_snapshot_id = f"{instance_id}-{datetime.now().strftime('%Y-%m-%d-%H-%M')}"

    rds.create_db_snapshot(
        DBSnapshotIdentifier=new_snapshot_id,
        DBInstanceIdentifier=instance_id
    )
