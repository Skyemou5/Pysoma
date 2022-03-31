
import os
import pathlib
import re

from pprint import pprint
from lib.dotenv import dotenv_values
import houdini_setup_shared as hs

env_file = pathlib.Path(pathlib.Path.cwd())/'.config/config.env'


# from houdini_setup_shared import env_from_file
# from houdini_setup_shared import seek_keys
# from houdini_setup_shared import houdini_env_setup
# from houdini_setup_shared import rs_setup

def rs_setup(env_path):
    env_dict = hs.env_from_file(env_path)
    hou_root = os.environ['HOU_ROOT']
    hou_path = pathlib.Path(hou_root)
    pattern = re.compile('/G[a-z]')
    hou_version = re.sub('[a-z]','',hou_path.name)
    print(f'houdini version:: {hou_version}')

    rs_check_key = [
        'USE_RS',
    ]
    rs_keys = [
        'RS_PATH',
        'HOUDINI_DSO_ERROR',
    ]

    rs_check_dict = hs.seek_keys(env_dict,rs_check_key)
    print(rs_check_dict)
    try:
        if(rs_check_dict['USE_RS']=='1'):
            rs_vars = hs.seek_keys(env_dict,rs_keys)
            print('use redshift for this project')
            os.environ['HOUDINI_DSO_ERROR']=rs_vars['HOUDINI_DSO_ERROR']
            os.environ['PATH']=str(rs_vars['RS_PATH']+':$PATH')
            os.environ['HOUDINI_PATH']=str(f'/usr/redshift/redshift4houdini/{hou_version};&')
        elif(rs_check_dict['USE_RS']=='0'):
            print('don\'t use redshift for this project')
        else:
            ValueError
    except ValueError:
        print('! There is an error with the env file and redshift.')
        quit()


def main():
    os.chdir(os.environ['HOU_ROOT'])
    rs_setup(env_file)
    env_dict = hs.env_from_file(env_file)
    print(f'Directory changed to --> {pathlib.Path.cwd()}')
    from houdini_setup_shared import key_list
    new_dict = hs.seek_keys(env_dict,key_list)
    hs.houdini_env_setup(env_dict)
    file_path = ''
    cmd = str('. ./houdini_setup')
    if(new_dict['OPEN_FILE']=='1'):
        file_path = str(new_dict['HIP']+'/'+new_dict['FILE_TO_OPEN'])
        cmd = cmd+str('&& houdini '+file_path)
    else:
        cmd = cmd+str(' && hconfig && houdini')
    os.system(cmd)



    #  && hconfig -ap
# if __name__ == "__main__":
#     main()

main()