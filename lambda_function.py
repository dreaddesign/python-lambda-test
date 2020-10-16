import sys
import logging
import psycopg2
import json
import os
import socket 
# rds settings
rds_host  = os.environ.get('host')
rds_username = os.environ.get('username')
rds_user_pwd = os.environ.get('password')
rds_db_name = os.environ.get('dbname')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn_string = "host=%s user=%s password=%s dbname=%s" % \
                    (rds_host, rds_username, rds_user_pwd, rds_db_name)
    conn = psycopg2.connect(conn_string)
except:
    logger.error("ERROR: Could not connect to Postgres instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS Postgres instance succeeded")

def lambda_handler(event, context):
    
    get_Host_name_IP() #Function call

    query = """select id, product_name, cron_name
            from cron_status"""

    with conn.cursor() as cur:
        rows = []
        cur.execute(query)
        for row in cur:
            rows.append(row)

    return { 'statusCode': 200, 'body': rows }

def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print("Hostname :  ",host_name)
        print("IP : ",host_ip)
    except:
        print("Unable to get Hostname and IP")

