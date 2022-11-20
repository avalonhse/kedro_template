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

#project_name = '{{ cookiecutter.project_name }}'

data_dirs = ["/01_raw","/02_intermediate","/03_primary","/06_models"]
check_paths(data_dirs, data_path)

