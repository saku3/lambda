
import os
import sys
import logging
import pymysql

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')


logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(DB_HOST, user=DB_USER,
                           passwd=DB_PASSWORD, db=DB_NAME, connect_timeout=5)
except:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


def lambda_handler(event, context):
    with conn.cursor() as cur:
        cur.execute("select * from users;")
        for row in cur:
            print(row)
