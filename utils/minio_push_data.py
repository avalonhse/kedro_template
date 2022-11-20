from dotenv import load_dotenv
from pathlib import Path

import os, yaml
from minio import Minio

dotenv_path = Path('../../data/config/.env')
load_dotenv(dotenv_path=dotenv_path)
MINIO_IP = str(os.getenv('MINIO_IP'))
MINIO_USER = str(os.getenv('MINIO_USER'))
MINIO_PASSWD = str(os.getenv('MINIO_PASSWD'))

def push_data_to_minio(data_path,project_name):

    client = Minio(MINIO_IP + ':9000',access_key=MINIO_USER,secret_key=MINIO_PASSWD,secure=False)
    bucket_name = "research"

    raw_dir = data_path+"/"+project_name+"/01_raw"
    for file in os.listdir(raw_dir):
        client.fput_object(bucket_name, "/"+project_name+"/01_raw/" + file,  raw_dir + "/" + file)

push_data_to_minio("../../data","test")