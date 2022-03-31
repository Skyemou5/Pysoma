import os
import pathlib
import re
import houdini_setup_shared as hs

env_file = pathlib.Path(pathlib.Path.cwd())/'.config/config.env'

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
            #os.environ['PATH']=str(rs_vars['RS_PATH']+':$PATH')
            os.environ['HOUDINI_PATH']=str(f'/Applications/redshift/redshift4houdini/{hou_version};&')
        elif(rs_check_dict['USE_RS']=='0'):
            print('don\'t use redshift for this project')
        else:
            ValueError
    except ValueError:
        print('! There is an error with the env file and redshift.')
        quit()


def main():
    app_dir = '/Applications/Houdini/Houdini18.5.759/Frameworks/Houdini.framework/Versions/18.5/Resources'
    env_d = hs.env_from_file(env_file)
    dotenvdict = dict(hs.unpack_dotenv(env_d))
    os.environ['HOU_ROOT']=dotenvdict['HOU_ROOT']
    print(os.environ['HOU_ROOT'])
    print(pathlib.Path.cwd())
    # newpath = pathlib.Path(pathlib.Path.root()) / str(os.environ['HOU_ROOT']+'/Frameworks/Houdini.framework/Versions/Current/Resources')
    # fullpath = newpath.resolve()
    # print(fullpath)
    os.chdir(app_dir)
    rs_setup(env_file)
    
    envfile_d = hs.env_from_file(env_file)
    env_dict = hs.unpack_dotenv(envfile_d)
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
        cmd = cmd+str(' && hconfig -ap && houdini')
    os.system(cmd)


main()