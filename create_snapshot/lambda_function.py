import os
import json
import boto3
import time
from datetime import datetime, timedelta, tzinfo


rds = boto3.client('rds')


def lambda_handler(event, context):
    instance_id = os.environ.get('INSTANCE_ID')
    response = create_snapshot(instance_id)


def create_snapshot(instance_id):
    new_snapshot_id = f"{instance_id}-{datetime.now().strftime('%Y-%m-%d-%H-%M')}"
    rds.create_db_snapshot(
        DBSnapshotIdentifier=new_snapshot_id,
        DBInstanceIdentifier=instance_id
    )
