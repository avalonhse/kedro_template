# cook@ecutter-$your-project/hooks/post_gen_project.py

def check_path(directory):
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)

def check_paths(dirs, common_path):
    for dir_name in dirs:
        check_path(common_path + dir_name)

import os
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace("\\","/")
data_path = parent_path + "/data/" + os.path.basename(os.getcwd())

data = "data_path : \"" + data_path + "\" "
with open("./conf/base/globals.yml", 'w') as f:
    f.write(data)

from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path(parent_path + '/data/config/.env')
load_dotenv(dotenv_path=dotenv_path)
MINIO_IP = str(os.getenv('MINIO_IP'))
MINIO_USER = str(os.getenv('MINIO_USER'))
MINIO_PASSWD = str(os.getenv('MINIO_PASSWD'))

data = "dev_minio: \n key: " +  MINIO_USER + " \n secret: " + MINIO_PASSWD + " \n client_kwargs: \n  endpoint_url : 'http://" + MINIO_IP + ":9000' "
with open("./conf/local/credentials.yml", 'a') as f:
    f.write(data)

data_dirs = ["/01_raw","/02_intermediate","/03_primary","/06_models"]
check_paths(data_dirs, data_path)

