import os
import pathlib
import re
from lib.dotenv import dotenv_values

key_list = [
        'HSITE',
        'HSITE_185',
        'HOUDINI_TERM',
        'DELIGHT',
        'OCIO',
        'PROJECT_ROOT',
        'REPO_ROOT',
        'PROJECT_CONFIG',
        'USER',
        'ASSETS_GLOBAL_ROOT',
        'G_HDA',
        'PACKAGES',
        'SHOTS_ROOT',
        'G_PRE_PRODUCTION',
        'SHOT_ROOT'
        'POST_RPODUCTION',
        'HIP',
        'HDA',
        'SHOT',
        'RENDER',
        'GEO',
        'TEXTURE',
        'REFERENCE',
        'OPEN_FILE',
        'FILE_TO_OPEN',
        'CREATE_FILE',
]

def env_from_file(path):
    #env_file = pathlib.Path(pathlib.Path.cwd())/'.config/config.env'
    dict_var = dotenv_values(path)
    #print(dict_var)
    return dict_var

def seek_keys(d, key_list):
    result = {}
    for k, v in d.items():
        if k in key_list:
            if isinstance(v, dict):
                #print(k + ": " + list(v.keys())[0])
                result[k]=list(v.keys())
            else:
                #print(k + ": " + str(v))
                result[k]=str(v)
        if isinstance(v, dict):
            seek_keys(v, key_list)
    return result

def unpack_dotenv(env_d):
    import lib.flatdict as flatdict
    result = flatdict.FlatDict(env_d,delimiter=':')
    return result

# def env_from_file(path):
#     #env_file = pathlib.Path(pathlib.Path.cwd())/'.config/config.env'
#     dict_var = dotenv_values(path)
#     #print(dict_var)
#     return dict_var

def houdini_env_setup(d):
    os.environ['JOB']=d['SHOT_ROOT']
    os.environ['HIP']=d['HIP']
    os.environ['HOUDINI_PACKAGE_DIR']=d['PACKAGES']
    os.environ['HSITE']=d['HSITE_185']
    os.environ['HOUDINI_MAX_BACKUP_FILES']='0'

