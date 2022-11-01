# cook@ecutter-$your-project/hooks/post_gen_project.py

import os
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace("\\","/")
data_path = parent_path + "/data/" + os.path.basename(os.getcwd())

data = "data_path : \""+data_path+"\" "
with open("./conf/base/globals.yml", 'w') as f:
    f.write(data)
