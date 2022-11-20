from dotenv import load_dotenv
from pathlib import Path

import os, yaml, sys
from minio import Minio

dotenv_path = Path('../../data/config/.minio_env')
load_dotenv(dotenv_path=dotenv_path)
MINIO_IP = str(os.getenv('MINIO_IP'))
MINIO_USER = str(os.getenv('MINIO_USER'))
MINIO_PASSWD = str(os.getenv('MINIO_PASSWD'))

def pull_data_to_minio(data_path,project_name):

    client = Minio(MINIO_IP + ':9000',access_key=MINIO_USER,secret_key=MINIO_PASSWD,secure=False)
    bucket_name = "research"

    for item in client.list_objects(bucket_name, recursive=True):
        client.fget_object(bucket_name,item.object_name, data_path+"/"+item.object_name)

pull_data_to_minio("../../data","hoang")