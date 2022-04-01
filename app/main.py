#!/usr/bin/python3

#region HEADER

import contextlib
from importlib.resources import path
#from msilib.schema import File
# from importlib.resources import path
# from lzma import _PathOrFile
# from operator import add
import os
import pathlib
import string
# import subprocess
import argparse
import fnmatch
import glob
import sys
import json
import lib.dotenv
import tkinter as tk
#import yaml
import re
# import logging
# import shlex
import argparse

#########################################
#########################################
#########################################
from pprint import pprint
from itertools import chain, repeat
from pathlib import Path, PurePath
from sys import platform, stderr, stdout
#from simple_term_menu import TerminalMenu
from lib.dotenv import dotenv_values, load_dotenv

##########################################
##########################################
##########################################
#endregion
#region VARIABLES

##############################
############ VARS ############
##############################

######## Default Hou paths #########
# Linux houdini_setup_bash         #
# mac houdini terminal             #
# win houdini command line tools   #
####################################


hou_18_paths = {
    "linux":"/opt/hfs18.5.759",
    "mac":"/Applications/Houdini18.5.759",
    "win":"C:\Program Files\Side Effects Software\Houdini 18.5.759"
    }

choose_project_root = ''

#inital setup check
INITIALIZED=''

#Team member name
USER: string = ''

#dates
INIT_DATE=''
CURRENT_DATE=''
LAST_OPENED=''
TIME_OPENED=''
TIMES_OPENED = []
DATES_OPENED = []

#houdini terminal
HOUDINI_TERM = ''

# config
CONFIG = ''

# Other vars
path_list = []
env_dict = {}

# System Paths
HOU_ROOT = ''

# 3Delight Path
DELIGHT = ''

# ACES path
OCIO = ''

# current shot
SHOT = ''

# preset paths
HOME = Path.home() # gets path for HOME variable

# app path
application_path = ''

# name
PROJECT_NAME = ''

# paths to set
PROJECT_ROOT = ''
SHOTS_ROOT = ''
ASSETS_GLOBAL_ROOT = ''

PACKAGES = ''
HDA_GLOBAL = ''

# PER SHOT VARS
BLEND = ''
GEO = ''
HIP = ''
RENDER = ''
REF = ''
TEXTURE = ''

#endregion
#region fix compile issues
if getattr(sys, 'frozen', False):
    import sys, os
    
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

REPO_ROOT = Path(application_path).parents[1]
dirslist = glob.glob("%s/*/" % REPO_ROOT)


#region HELPER METHODS
#region Directory Setup helper methods
###############################
####### DIRECTORY PATHS #######
###############################

def unpack_dotenv(env_d):
    import lib.flatdict as flatdict
    result = flatdict.FlatDict(env_d,delimiter=':')
    return result

def add_dict_to_dict(sd,td):
    for k, v in sd.items():
        print(k)
        td[k]=v


def get_path(root,target):
    new_path = PurePath(root,target)
    return new_path

def add_var_to_dict(k,v):

    env_dict[k]=v

def add_to_arr(obj):
    path_list.append(obj)

def add_to_dict_and_arr(k,v):
    add_var_to_dict(k,v)
    add_to_arr(v)

def add_dirlist_to_return_dict(list):

    k = ''
    v = ''
    dict = {}
    for i in list:

        if (i.is_dir() == True):
            k = i.name
            v = i

            dict[k]=v
        else:
            continue
    return dict

def create_dir_if_not_present(dirpath):

    if not dirpath.exists():
        print(f'+D/..........................Creating new {dirpath.name} Directory in {dirpath.parent}...')
        pathlib.Path(dirpath).mkdir(parents=True,exist_ok=True)
    else:
        print(f'!!!--------------Directory {dirpath.name} in {dirpath.parent} exists! Skipping...')

    

def create_dirs_from_list(currpath,dirlist) -> list:
    """
    takes the current path as a path obejct and a list of strings 
    created the child directories based on the list of strings
    returns an array of the paths of the newly created child dirs
    if dirs already exist grap the paths and export them
    """
    newpathlist = []
    for d in dirlist:
        newdirpath = pathlib.Path(currpath)/d
        

        create_dir_if_not_present(newdirpath)
        try:
            if newdirpath.exists():
                newpathlist.append(newdirpath)
        except:
            print('could not add child dir to list!')
    return newpathlist

def env_from_file(path):
    #env_file = pathlib.Path(pathlib.Path.cwd())/'.config/config.env'
    dict_var = dotenv_values(path)
    #print(dict_var)
    return dict_var


def add_dirlist_to_dict(dirlist,nameprefix):
    '''Add a list to a dictionary and add a prefix to key'''

    for d in dirlist:
        k = f'{nameprefix}{d.name}'

        add_to_dict_and_arr(k,d)

def is_empty(folder: Path) -> bool:
    return not any(folder.iterdir())

# create empty file in empty dir for git
def add_file_to_empty_folder(path):
    if is_empty(path):
        fp = pathlib.Path(path)/'.gitkeep'
        fp.open("w",encoding="utf-8")

def add_readme_file_to_dir(path):
    #check if git file exists
    # gitfile = pathlib.Path(path)/'.gitkeep'
    # if gitfile.exists():
    #     print('git file exists')
    #     gitfile.unlink()
    print(f'+f/...................................................................creating README file in {path.name}...')
    fp = pathlib.Path(path)/'README.md'
    fp.open("w",encoding="utf-8")

def add_files_to_empty_folders(dirlist):
    for d in dirlist:
        #print(d)
        add_file_to_empty_folder(d)


#endregion
#region Dir and Config helper methods

###################################
####### Dir & Config Stuff ########
###################################

# config stuff
def create_config_dir():
    #global CONFIG
    p = Path(env_dict['PROJECT_ROOT'])/'.config'
    if not Path.is_dir(p):
        Path.mkdir(p)
        add_var_to_dict('CONFIG_DIR',p)
        return p
        #CONFIG = p
    else:
        add_var_to_dict('CONFIG_DIR',p)
        return p

# check OS
def check_os():
    platform = ''
    from sys import platform
    if platform == "linux" or platform == "linux2":
        # linux
        print("Congrats! You are on linux!")
        platform = "linux"
        add_var_to_dict('OS','linux')
        #return
        pass
    elif platform == "darwin":
        # OS X
        print("You are on OSX")
        platform = "mac"
        add_var_to_dict('OS','mac')
        #return
        pass
    elif platform == "win32":
        # Windows...
        print("You are, unfortunately on Windows...")
        platform = "win"
        add_var_to_dict('OS','win')
        #return
        pass
    else:
        print("I don't know what system you're on...")
        pass
    return platform

def subdirList(rootDir):
    rootdirlist = glob.glob("%s/*/" % rootDir)
    return rootdirlist

def initDirList(list):
    for item in list:
        pp = pathlib.PurePath(item)
        pathname = "G_" + pp.name
        #print(pathname)
        add_to_dict_and_arr(pathname,item)

def no_subdirs(rootdir) -> bool:
    checklist=[]
    for p in pathlib.Path(rootdir).iterdir():
        checklist.append(p.is_dir())
    if True in checklist:
        return False
    else:
        return True

def count_subdirs(rootdir):
    total = ''
    subdirlist = []
    total = len(os.walk(rootdir).next()[1])
    #print(total)
    return total

#endregion
#region User Input Helper funcs

# question stuff
def y_n_q(q) -> bool:
    '''
    give question
    keep asking question with invalid input
    if the input is yes return true
    if the input is no return false
    '''
    result=''
    while True:
        try:
            user_choice = input(f'{q} y/n: ').lower()
            if(user_choice == 'y'):
                return True
            elif(user_choice == 'n'):
                return False
            else:
                raise ValueError
        except ValueError:
            print('Invalid input. Please try again...')
            continue

#endregion
#endregion
#region WORK SETUP METHODS
#region config files

def convert_env_dict_to_string():

    new_d = {}

    for k, v in env_dict.items():

        new_d[k]=v
        if v is not isinstance(v, str):

            new_v = str(v)
            new_d[k]=new_v

    return(new_d)


def convert_env_dict_to_path(env_d):
    new_d = {}
    for k, v in env_d.items():

        if isinstance(v, str):

            new_v = pathlib.Path(v)

            new_d[k]=new_v
        else:

            new_d[k]=v

    return new_d

def write_to_env_file(env_d):
    new_d = convert_env_dict_to_string()
    path_d = convert_env_dict_to_path(env_d)
    #pprint(path_d)
    fp = Path(path_d["CONFIG"]) / "config.env"

    with fp.open("w",encoding="utf-8") as f:
        for key, value in path_d.items():
            f.write('%s="%s"\n' % (key, value))


def write_to_json():
    path_d = convert_env_dict_to_path()
    string_d = convert_env_dict_to_string(env_dict)
    fp = Path(path_d["CONFIG"]) / "config.json"

    with fp.open("w") as f:
        f.write(json.dump(string_d,fp, indent=4,sort_keys=True))
    

#region Config setup

def create_config_files(env_d):
    path = env_d['CONFIG_DIR']
    try:
        if path.is_dir():
            print(path)
            write_to_env_file(env_d)
            #write_to_json()
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        input('Something went wrong finding the config folder')
        quit()

#endregion
#region User data

#TODO finish caching user data

def user_info():
    user_choice = input(
        'Please enter your name. '
    ).lower()
    user_confirm = input(
        f'Is {user_choice} correct? y/n: '
    ).lower()
    if user_confirm == 'y':
        return user_choice
    elif user_confirm == 'n':
        user_info()


def project_settings_file(fp):
    # config stuff

    try:
        if is_file_empty(fp):
            #print('file is empty...')
            pass

        else:
            pass


    except FileNotFoundError:
        print('creating project config file...')
        fp.open("w",encoding="utf-8")
        
        project_settings_file(fp)
    # with fp.open("w",encoding="utf-8") as f:
    # for key, value in path_d.items():
    #     f.write('%s="%s:&"\n' % (key, value))

def read_write_project_data(func):
    def inner(fp,dict):
        pass

def user_init(configpath):
    namelist = []
    namedict = []
    user = user_info()
    add_to_dict_and_arr('USER',user)
    fp = pathlib.Path(configpath)/'.projectdata.yaml'
    project_settings_file(fp)

def is_file_empty(file_name) -> bool:
    """ Check if file is empty by reading first character in it"""
    # open ile in read mode
    with open(file_name, 'r') as read_obj:
        # read first character
        one_char = read_obj.read(1)
        # if not fetched then file is empty
        if not one_char:
            return True
    return False

#endregion
#endregion
#region Check 3rd party software
#region Redshift setup

redshift_paths = {
    'windows':'C:/ProgramData/Redshift/bin',
    'mac':'/Applications/redshift/redshift4houdini/',
    'linux':'/usr/redshift/bin',
}

redshift_vars = {
    'HOUDINI_DSO_ERROR':2
}

def redshift_setup():
    platform = check_os()
    add_var_to_dict('HOUDINI_DSO_ERROR',str(2))
    rs_key = 'RS_PATH'
    add_var_to_dict(rs_key,redshift_paths[platform])
    rs_path = pathlib.Path(redshift_paths[platform])
    add_var_to_dict('USE_RS',str(1))
    return rs_path


def redshift_main():
    if(y_n_q('Is this project using Redshift?')):
        if(y_n_q('Do you have Redshift installed?')):
            rs_path = redshift_setup()
            try:
                if(rs_path.is_dir()):
                    redshift_setup()
                else:
                    FileNotFoundError
            except FileNotFoundError:
                print('Redshift installation not found... please check your install and try again')
                quit()
        else:
            print('please install redshift and try again...')
            quit()
    else:
        add_var_to_dict('USE_RS',str(0))
        print('Your config will be set to not use redshift... \n if you want to change this, initialize the project again...')



#endregion
#region 3DELIGHT setup

def delight_setup():
    global DELIGHT
    if os.environ.get("DELIGHT") is not None:
        print("Congrats! You have 3Delight installed!")
        DELIGHT = os.environ.get("DELIGHT")
        add_to_dict_and_arr("DELIGHT",DELIGHT)
    else:
        print("You don't have 3Delight installed! \n Please install it, and configure it for ACES.")
        sys.exit("Please isntall 3Delight then try again. Thanks!")


#endregion
#region ACES setup

def aces_check():
    global OCIO
    if os.environ.get("OCIO") is not None:
        print("Congrats! You have ACES configured correctly!")
        OCIO = os.environ.get("OCIO")
        add_to_dict_and_arr("OCIO",OCIO)
    else:
        print("You don't have ACES installed or need to fix the installation!")
        sys.exit("Please configure ACES and try again. Thanks!")
        


#endregion
#endregion

#region Directory Definitions

###########################################
########### folder dir lists ##############
###########################################

#region global dir names

###################################################
############# Global resource dirs ################
###################################################



'''project root global asset directories'''
global_asset_child_dir_namelist = [
    'SRC',
    'GEO',
    'BLEND',
    'TEXTURE',
    'HDA',
    'OTHER',
    'PDG',
    'USD',
    'POST_PRODUCTION',
]



###### POST stuff
global_asset_post_dir_namelist = [
    'Audio',
    'Compositing',
    'Reference',
    'Texture',
    'Project_Files',
    'Nuke',
    'Other',
    'Export'

]

post_comp_dir_namelist = [
    'LUTs',
    'Color_Scripts',
    'Project_Files',
    'Other'
    'Export'
]

post_audio_dir_namelist = [
    'SFX',
    'Music',
    'Reference',
    'Project_Files',
    'Other'
]

post_tex_dir_namelist = [
    'Data_Textures',
    'Alphas',
    'Masks',
    'PBR',
    'Grunge',
    'Substance'
    'Project_Files'
    'Other'
]

# Global Post folder

global_post_dir_namelist = [
    'Audio',
    'Compositing',
    'Reference',
    'Texture',
    'Project_Files',
    'Nuke',
    'Render',
    'Shots',
    'Scenes',
    'Other',
    'Export'
]

post_app_list = [
    'Fusion',
    'Nuke',
    'Resolve',
    'Adobe'
]

tex_app_list = [
    'Affinity',
    'Adobe',
    'Krita',
    'Gimp',
    'Other'
]

audio_app_list = [
    'Pro_Tools',
    'Ableton',
    'Bitwig',
    'Reaper',
    'Reason',
    'Other'
]

comp_app_list = [
    'Fusion',
    'Resolve',
    'Nuke',
    'Adobe'
]

######## CG stuff
'''global src subdirectories'''
global_src_dir_namelist = [
    'Blender',
    'Maya',
    'ZBrush',
    'Substance',
    'Other'
]
'''global geo subdirectories'''
global_geo_dir_namelist = [
    'FBX',
    'OBJ',
    'Houdini',
    'USD',
    'Cache',
    'Other'
]
'''global texture subdirectories'''
global_tex_dir_namelist = [
    'HDRI',
    'Imperfections',
    'PBR',
    'Data_Textures',
    'Decals',
    'Substance',
    'Alphas',
    'Masks',
    'Grunge',
    'OTHER',
]

#endregion
#region init folder helper functions

# def init_folders(path,name,subdirs,add_to_dict,pref,key):
#     parent = Path(path)/name
#     create_dir_if_not_present(parent)
#     try:
#         #if subdirs is not None:
#         add_readme_file_to_dir(parent)
        
#         #else:
#         #    pass
#     except ValueError:
#         pass
#     try:
#         if(add_to_dict == True):
#             try:
#                 add_to_dict_and_arr(key,parent)
#             except ValueError:
#                 pass
#     except ValueError:
#         pass
#     try:
#         subdirlist = create_dirs_from_list(parent,subdirs)
#         try:
#             add_dirlist_to_dict(subdirlist,pref)
#         except ValueError:
#             pass
#     except ValueError:
#         pass

def init_folder(parent_path,name):
    path = pathlib.Path(parent_path)/name
    create_dir_if_not_present(path)
    add_readme_file_to_dir(path)
    return path

def init_nested_folder(parent_path,dirlist):
    return create_dirs_from_list(parent_path,dirlist)

def register_init_folder(path,key):
    add_var_to_dict(key,path)

def register_nested_folders(dirlist,prefix,env=False):
    key = ''
    upper = []
    add_dirlist_to_dict()
    if (env == True):
        for i in dirlist:
            new_name = str(i.name).upper()
            sliced_path = i.parts[:-1]
            new_path = pathlib.Path(sliced_path)/new_name
            upper.append(new_path)
        add_dirlist_to_dict(upper,prefix)
    else:
        add_dirlist_to_dict(dirlist,prefix)

#endregion
###########
#endregion
#region SHOTS
#region shot subdir definition

#TODO change this to json
#TODO add R&D to shots

###########################################
##############               ##############
############     Shot Prep     ############
##############               ##############
###########################################
#region Shot dir names
'''shot subdirectories'''
shot_subdir_names = [
    "GEO",
    "SRC",
    "HIP",
    "RENDER",
    "TEXTURE",
    "BLEND",
    "ASSETS",
    "HDA",
    "PDG",
    "USD",
    "REFERENCE",
    "RESEARCH_AND_DEVELOPMENT",
    "LOOKDEV",
    "POST_PRODUCTION",
    "PRE_PRODUCTION",
    "FINAL",
    'SCRIPTS',
    "CLIPS",
    "VEX",
    "OTHER",
]

# Post fx shot stuff
shot_post_dirnames = [
    'Audio',
    'Compositing',
    'Editing',
    'Texture',
    'Project_Files',
    'Export',
]

shot_audio_dirnames = [
    'SFX',
    'Music',
    'Reference',
    'Project_Files',
]

shot_comp_dirnames = [
    'LUTs',
    'Color_Scripts',
    'Project_Files',
    'Fusion',
    'Nuke',
    'Adobe',
    'Other',
    'Export',
]


shot_tex_post_dirnames = [
    'Data_Textures',
    'Alphas',
    'Masks',
    'PBR',
    'Grunge',
    'Substance',
    'Project_Files',
    'Other',
]
#endregion
#endregion
#region Create Shot
####
shots_list = []
shot_env_dict = {}

def create_shot():
    '''
    Check if first shot folder exists, if not, create it. If folders exists count them and create a new one incremented
    '''

    #ensure top-level 'shots' exists
    #top_level_shot = Path(Path(Path.cwd().parent)) / "Main_Project/shots"
    #TODO fix this
    top_level_shot = Path(env_dict['PROJECT_ROOT']) / "Shots"
    if not Path.is_dir(top_level_shot):
        Path.mkdir(top_level_shot)

    #case 1 - creating first shot directory
    first_shot_n = Path(top_level_shot)/'shot_1'
    if not Path.is_dir(first_shot_n):
        Path.mkdir(first_shot_n)
        shot_subfolders = create_shot_subfolders(first_shot_n)


        print(f'{first_shot_n.name} created...')
        
        add_to_dict_and_arr('SHOT_ROOT',first_shot_n)
        
        #shot_env_var_init(first_shot_n,shot_subfolders)
        print(f"\'{first_shot_n}\' created along with resource dirs.")
        return shot_subfolders, first_shot_n
    #case 2 - creating any subsequent shot directory
    else:
        shot_n = first_shot_n
        #skip existing shot directories...
        while Path.is_dir(shot_n):
            try:
                shot_name = shot_n.name
                #incremented_number = int(shot_n.name.parts[1].split('_')[1])+1
                incremented_number = int(shot_name.split('_')[1])+1
                updated_shot_n = shot_n.parts[2].replace(shot_n.parts[2].split('_')[1],str(incremented_number))
                shot_n = Path.joinpath(Path(shot_n.parts[1]), Path(updated_shot_n))
                shot_n = Path("./Main_Project")/shot_n
            except:
                raise Exception("!! couldn't increment appended folder number")

        #make the new shot directory...
        Path.mkdir(shot_n)
        shots_list.append(shot_n)
        #create resources for the new shot directory
        shot_subfolders = create_shot_subfolders(shot_n)
        
        add_to_dict_and_arr('SHOT_ROOT',shot_n)

        

        # if y_n_q("would you like to open newly created shot?"):
        #     open_shot(shot_n)
        # else:
        #     shotlist = subdir_list(top_level_shot)
        #     print(shotlist)
        
        print(f"\'{shot_n}\' created along with resource dirs.")
        return shot_subfolders, shot_n

def create_shot_subfolders(rootdir):
    dirlist = create_dirs_from_list(rootdir,shot_subdir_names)
    add_readme_file_to_dir(rootdir)
    global global_src_dir_namelist,global_geo_dir_namelist,global_tex_dir_namelist
    subsubresdict = {
        'SRC':global_src_dir_namelist,
        'GEO':global_geo_dir_namelist,
        'TEXTURE':global_tex_dir_namelist,
    }

    specresdict={}

    for a in dirlist:
        specresdict[a.name]=a
    for d in dirlist:
        for k, v in subsubresdict.items():
            if d.name == k:
                curr_dir = specresdict[k]
                print(f'++D.......creating subresource folders in {k}...')
                subsubdirlist = create_dirs_from_list(specresdict[k],v)
                add_readme_file_to_dir(specresdict[k])
                add_files_to_empty_folders(subsubdirlist)
    
    global pre_prod_dir_names, shot_post_dirnames, comp_app_list, shot_audio_dirnames, shot_comp_dirnames, shot_tex_post_dirnames

    #pre production
    shot_pre_dir = Path(rootdir)/'PRE_PRODUCTION'
    add_readme_file_to_dir(shot_pre_dir)
    shot_pre_sub_list = create_dirs_from_list(shot_pre_dir,pre_prod_dir_names)
    add_files_to_empty_folders(shot_pre_sub_list)

    #post sub
    post_prod_path = Path(rootdir)/'POST_PRODUCTION'
    add_readme_file_to_dir(post_prod_path)
    post_prod_list = create_dirs_from_list(post_prod_path,shot_post_dirnames)
    #post proj
    post_proj_path = Path(post_prod_path)/'Project_Files'
    add_readme_file_to_dir(post_proj_path)
    post_proj_list = create_dirs_from_list(post_proj_path,comp_app_list)
    add_files_to_empty_folders(post_prod_list)
    #audio sub
    post_aud_path = Path(post_prod_path)/'Audio'
    add_readme_file_to_dir(post_aud_path)
    post_aud_list = create_dirs_from_list(post_aud_path,shot_audio_dirnames)
    #audio proj
    aud_proj_path = Path(post_aud_path)/'Project_Files'
    add_readme_file_to_dir(aud_proj_path)
    aud_proj_list = create_dirs_from_list(aud_proj_path,audio_app_list)
    add_files_to_empty_folders(post_aud_list)
    add_files_to_empty_folders(aud_proj_list)
    #comp sub
    comp_path = Path(post_prod_path)/'Compositing'
    add_readme_file_to_dir(comp_path)
    comp_list = create_dirs_from_list(comp_path,shot_comp_dirnames)
    #comp proj
    comp_proj_path = Path(comp_path)/'Project_Files'
    add_readme_file_to_dir(comp_proj_path)
    comp_proj_list = create_dirs_from_list(comp_proj_path,comp_app_list)
    add_files_to_empty_folders(comp_list)
    add_files_to_empty_folders(comp_proj_list)
    #tex sub
    post_tex_path = Path(post_prod_path)/'Texture'
    add_readme_file_to_dir(post_tex_path)
    post_tex_list = create_dirs_from_list(post_tex_path,shot_tex_post_dirnames)
    #tex proj
    post_tex_proj_path = Path(post_tex_path)/'Project_Files'
    add_readme_file_to_dir(post_tex_proj_path)
    post_tex_proj_list = create_dirs_from_list(post_tex_proj_path,tex_app_list)
    add_files_to_empty_folders(post_tex_list)
    add_files_to_empty_folders(post_tex_proj_list)

    #get any loose empty folders
    add_files_to_empty_folders(dirlist)
    
    return dirlist

#endregion
#region Open Shot
#region open shot helpers
def get_resource_paths(curr_path):
    path = curr_path
    path_list = []
    for p in Path(path).iterdir():
        if(p.is_dir()==True):
            #print(f'creating {p.name} directory...')
            path_list.append(p)
        else:
            #print('file')
            continue
    #print(path_list)
    return path_list

def check_if_num_in_list(num,list) -> bool:
    result = False
    total = len(list)
    if (num > 0) and (num < len(list)+1):
        result = True
    else:
        result = False
    return result

#endregion

def subdir_list(path):

    shots_only=[]
    sorted_shots=[]
    sorted_shot_names=[]
    shot_name_list=[]
    if any(Path(path).iterdir()):

        for p in Path(path).iterdir():
            if p.is_dir():
                shot_name_list.append(p.name)
        shots_only = [x for x in shot_name_list if re.match(r"^shot_\d+$", x)]
        sorted_shot_names = sorted(shots_only,key=lambda x: x.split('_')[1])
        #print(f'sorted shots::: {sorted_shot_names}')
        for p in sorted_shot_names:
            np = pathlib.Path(path)/p
            sorted_shots.append(np)
    return sorted_shots

def choose_shot(pathlist):
    '''
    displays number of choices user and input
    '''
    choices = []
    choice = ''
    for i in range(len(pathlist)):
        print(f'{i+1} = {pathlist[i].name}')
        choices.append(i+1)
    print(f'Choices:: {choices}')
    choice = user_choose_shot(choices)
    return choice

def user_choose_shot(list):
    '''
    Takes a list
    Returns the index chosen by user if valid
    also returns user confirmation
    '''
    # returns
    choice = 0
    confirm = False
    # other
    inner_confirm = True
    #result = ''
    while True:
        try:
            choice = int(input('Please type the corresponding number of the shot you wish to open: '))
            result = check_if_num_in_list(choice,list)
            if (result == True):
                print(f'You chose shot_{choice}')
                while inner_confirm:
                    try:
                        #accepted_input = ['y','n']
                        user_confirm = input(
                            'Is this correct? y/n: '
                        ).lower()
                        if (user_confirm == 'y' or 'n'):
                            if(user_confirm == 'y'):
                                confirm = True
                                inner_confirm = False
                            elif(user_confirm == 'n'):
                                confirm = False
                                inner_confirm = False
                            else:
                                print('Invalid response, try again...')
                                raise ValueError                          
                        else:
                            raise ValueError
                    except ValueError:
                        print('Invalid response, try again...')
                        continue
                if(confirm == True):
                    break
                elif(confirm == False):
                    break
            else:
                print('Invalid response, try again...')
                continue
        except ValueError:
            print('Invalid response, try again...')
            continue
    return choice, confirm

def shot_decision():
    #TODO refactor into while lop with try except
    '''
    Asks user if they want to create a new shot or open an existing shot
    if they want to open an existing shot and no shot exists it is created and automatically opened
    if they created a new shot, the shot folder number is automatically incrimented
    then they are asked which shot to open
    '''
    shots_root = pathlib.Path(env_dict['PROJECT_ROOT'])/'Shots'
    shot_root_empty = no_subdirs(shots_root)
    shot_choice_path = ''
    shot_root = ''
    shot_choice = ''
    User_not_confirm = True
    shot_chosen = False
    while User_not_confirm:
        try:
            user_choice = int(input(
                '1 - Create a new shot \n2 - Open existing shot \n'
            ).lower())
            
            # Case 1 
            if user_choice == 1:
                #TODO add support for continuing to make shots
                #TODO support for shot naming?
                print('creating new shot....')

                shot_folders = create_shot()
                if y_n_q("Would you like to open newly created shot?"):
                    newshot = shot_folders[1]
                    newshotnum = int(newshot.name.split('_')[1])
                    print(newshotnum)
                    shot_choice_path = newshot
                    shot_chosen = True
                    break
                else:
                    if y_n_q('Do you want to open an existing shot?'):
                        shotlist = subdir_list(shots_root)
                        while True:
                            try:
                                shot_choice = choose_shot(shotlist)
                                if (shot_choice[1] == False):
                                    continue
                                elif (shot_choice[1] == True):
                                    print(f'shot choice:: {shot_choice[0]} ---')
                                    shot_choice_path = shotlist[shot_choice[0]-1]
                                    User_not_confirm = False
                                    break
                                else:
                                    raise ValueError
                            except ValueError:
                                continue
                            # select shot
                            # then houdini stuff
                    else:
                        print('you must choose a shot before opening houdini...')
                        quit()
            # case 2
            elif user_choice == 2:
                '''
                if no shot exists create it
                since there would only be one select that folder
                then go to houdini stuff
                '''
                print('please choose which shot to open...')
                if no_subdirs(shots_root):
                    print('No shots exist! Creating shot_1 first...')
                    shot_folders = create_shot()
                    print('Choosing newly created shot_1...')
                    p = Path(shots_root)/'shot_1'
                    shot_choice_path = p
                    break
                    #print(p)
                    #open_shot(p)
                else:
                    shotlist = subdir_list(shots_root)
                    while True:
                        try:
                            shot_choice = choose_shot(shotlist)
                            if (shot_choice[1] == False):
                                print(shot_choice[1])
                                
                                continue
                            elif (shot_choice[1] == True):
                                print(f'shot choice:: {shot_choice[0]} ')
                                shot_choice_path = shotlist[shot_choice[0]-1]
                                User_not_confirm = False
                                break
                                #open_shot(shot_choice_path)
                            else:
                                raise ValueError
                        except ValueError:
                            continue
            else:
                raise ValueError
        except ValueError:
            print('Please enter the numbers 1 or 2...')
            continue
    
    open_shot(shot_choice_path)

def open_shot(path):
    '''
    after user has confirmed shot folder do this...
    '''
    env_dict['SHOT_ROOT']=path
    reslist = []
    #print(path)
    subdir_list = get_resource_paths(path)
    for i in subdir_list:
        reslist.append(i)
        print(f'+------------------Registering directory {i.name} in {path.name} directory for your session...')
    print(f'!!! ----- Here is a reminder of the subdirectories in your resources folder ----- !!!')
    
    add_dirlist_to_dict(reslist,'')
    
    for i in reslist:
        
        sublist = []
        print(i.name)
        for k in i.iterdir():
            if k.is_dir():
                print(f'...........{k.name}')
                sublist.append(k)
    
    
    # shot_env_dict(path,subdir_list)
    #shot_env_var_init(path,reslist)

#region Houdini file

hip_file_ext = [
    'hip',
    'hipnc',
    'hiplc',
]


def list_proj_files(directory):
    p = directory
    file_list = []
    choice_list = []
    # for f in os.listdir(p):
    #     print(f)
    try:
        for f in os.listdir(p):
            if not f.startswith('.'):
                
                file_list.append(f)
    except FileNotFoundError: 
        print('No hip files found')
    
    for i in range(len(file_list)):
        print(f'{i+1}:: {file_list[i]}')
        choice_list.append(i+1)
    print(choice_list)
    return file_list           

def choose_file(flist):
    '''
    displays number of choices user and input
    '''
    choices = []
    choice = ''
    for i in range(len(flist)):
        print(f'{i+1} = {flist[i]}')
        choices.append(i+1)
    print(f'Choices:: {choices}')
    choice = user_choose_file(choices)
    return choice

def user_choose_file(choices):
    inner_confirm = True
    confirm = False
    choice = 0
    while True:
        try:
            user_choice = int(input('Please select a corresponding number for the file you wish to open: ').lower())
            #print(proj_list[user_choice])
            result = check_if_num_in_list(user_choice,choices)
            if(result == True):
                print(f'You chose: {choices[user_choice-1]}')
                while inner_confirm:
                    try:
                        #accepted_input = ['y','n']
                        user_confirm = input(
                            'Is this correct? y/n: '
                        ).lower()
                        if (user_confirm == 'y' or 'n'):
                            if(user_confirm == 'y'):
                                confirm = True
                                inner_confirm = False
                            elif(user_confirm == 'n'):
                                confirm = False
                                inner_confirm = False
                            else:
                                print('Invalid response, try again...')
                                raise ValueError                          
                        else:
                            raise ValueError
                    except ValueError:
                        print('Invalid response, try again...')
                        continue
                if(confirm == True):
                    break
                elif(confirm == False):
                    break
            else:
                print('Invalid response, try again...')
                continue
        except ValueError:
            print('Invalid response, try again...')
            continue
    return choice, confirm


def houdini_file_main():
    hip_root = pathlib.Path(env_dict['HIP'])
    proj_list = list_proj_files(hip_root)

    if not (len(proj_list) == 0):
        print(proj_list)
        if(y_n_q('Do you want to open an existing file?')):
            choice = choose_file(proj_list)
            add_var_to_dict('OPEN_FILE',1)
            #print(choice)
            file_choice = proj_list[choice[0]]
            print(f'You chose {file_choice} to open....')
            add_var_to_dict('FILE_TO_OPEN',file_choice)
            #choice = choose_file()
        else:
                add_var_to_dict('OPEN_FILE',0)
                print('Create a new file after Houdini launches...')
                add_var_to_dict('FILE_TO_OPEN','')
                input('Press Enter to continue....')
    else:
        print('There are no project files in HIP directory, create one after houdini launches... \n')
        add_var_to_dict('OPEN_FILE',0)
        add_var_to_dict('FILE_TO_OPEN','')
        input('Press Enter to continue....')



#endregion
#region Hou shot env setup
def shot_env_var_init(shot_path,shot_dirlist):
    # add_readme_file_to_dir(shot_root)
    # shot_resource_list = get_resource_paths(shot_root)
    # for i in shot_dirlist:
    #     shot_env_dict[i.name]=i
    # pprint(shot_env_dict)
    add_dirlist_to_dict(shot_dirlist,'')
    #shot_dict = add_dirlist_to_return_dict(shot_resource_list)
    #print(f'Shot dict:::: {shot_dict}')
    # configure hou vars from existing paths
    # packages
    # HDAs
    # vars HSITE, HOUDINI_PACKAGE_DIR, JOB, HIP, HOUDINI_OTL_SCAN_PATH, HOUDINI_NO_ENV_FILE
    #print(shot_path)
    add_var_to_dict('SHOT_NAME',shot_path.name)
    #add_var_to_dict('HOUDINI_NO_ENV_FILE',True)
    add_var_to_dict('HSITE',env_dict['HSITE'])
    add_var_to_dict('HOUDINI_PACKAGE_DIR',env_dict['PACKAGES'])
    add_var_to_dict('JOB',shot_path)
    #hda_paths = env_dict['G_HDA']+':'+env_dict['HDA']
    hda_paths = str(f'{env_dict["G_HDA"]};{env_dict["HDA"]}')
    add_var_to_dict('HOUDINI_OTLSCAN_PATH',hda_paths)
    add_var_to_dict('HOUDINI_SCRIPT_PATH',env_dict['SCRIPTS'])
    add_var_to_dict('HOUDINI_TEXTURE_PATH',env_dict['TEXTURE'])
    add_var_to_dict('HOUDINI_GEOMETRY_PATH',env_dict['GEO'])
    add_var_to_dict('HOUDINI_CLIP_PATH',env_dict['CLIPS'])
    add_var_to_dict('HOUDINI_VEX_PATH',env_dict['VEX'])
    #print(hda_paths)
    #add_var_to_dict('HIP',shot_env_dict['HIP'])

    # aces stuff


    # resource_paths = [i[0] for i in os.walk(
    #     curr_path) if pathlib.Path.name(str(i[0])) in shot_subdir_names]
    # return resource_paths
    # List hip files
    # open hip files

#endregion
#endregion
#endregion
#endregion
#region HOUDINI 
##############################
####### Houdini Stuff ########
##############################
#region HOUDINI setup

def indie_check():
    '''Check if user has the correct houdini installed'''
    if y_n_q("Do you have houdini indie?"):
        print('Great!')
    else:
        print("You will need to convert your hdas and project files to indie using you're project leads account on orbolt before you push changes!")
        print("please check the docs for link to the converter!")
    if y_n_q("Do you have a python 3 version of houdini installed?"):
        print('Great!')
    else:
        print("please install a python 3 version of houdini 18.5.759 and then run this tool again!")
        print('Thanks!')
        sys.exit()


def load_from_config():
    from lib.dotenv import load_dotenv
    load_dotenv("./.config/config.env")

def getHouRoot():
    os = check_os()
    #print(os)
    path = hou_18_paths[os]
    #print(path)
    return path

#endregion

#region HOUDINI shell
# CMD prompt & BASH & CSH

###################################################
############## Get Houdini Terminal ###############
###################################################

def source_houdini():
    platform = check_os()
    path = pathlib.Path(hou_18_paths[platform])
    new_path = ''
    if platform == 'win':
        term = 'bin/hcmd.exe'
        new_path = pathlib.Path(path) / term
    elif platform == 'mac':
        term = 'Frameworks/Houdini.framework/Versions/Current/Resources/houdini_setup'
        new_path = pathlib.Path(path) / term
    elif platform == 'linux':
        term = 'houdini_setup'
        new_path = pathlib.Path(path) / term
    #print(new_path)
    return new_path

#region Houdini final
#####################################################
################### Houdini Final ###################
#####################################################

def set_env_vars(dictionary):
    for k,v in dictionary.items():
        prog = re.compile('[^&+]')
        #new_v = re.match(r"[^&+]",v)
        v_len = len(v)
        #new_v = str.rstrip(v[-1])
        new_v = re.sub(r"[:&+]",'', v)
        #print(k,new_v)
        os.environ[k]=new_v

def env_from_file():
    env_file = pathlib.Path(env_dict['CONFIG'])/'config.env'

    env_dict_file = lib.dotenv.dotenv_values(env_file)
    set_env_vars(env_dict_file)

def init_houdini():
    # This variable is necessary on H19.0.455 due to Houdini bug
    #compat = "export LD_PRELOAD=/lib/x86_64-linux-gnu/libc_malloc_debug.so.0 ; "
    cmd = []
    #cmd.append(compat)
    cmd.append("export JOB=\"%s\" ; " % SHOT)
    # Create env vars for project sub-directories
    # for dir in DIRS:
    #     cmd.append("export %s=\"%s/%s\" ; " % (dir,SHOT,dir))
    return cmd

##### HOUDINI MAIN #####
def houdini_main():
    #env_from_file()
    #print(f'env: {os.environ["HOUDINI_TERM"]}')
    env_file = pathlib.Path(env_dict['CONFIG'])/'config.env'
    #slurp_term()
    # load_from_config()
    cmd = []
    hou_setup = env_dict['HOUDINI_TERM']
    #local_os = check_os()
    if (env_dict['OS'] == 'win'):
        import houdini_setup_windows
    elif (env_dict['OS'] == 'mac'):
        import houdini_setup_mac
    elif (env_dict['OS'] == 'linux'):
        os.environ['HOU_ROOT']=str(env_dict['HOU_ROOT'])
        print(os.environ['HOU_ROOT'])
        import houdini_setup_linux
    else:
        pass


def hou_linux_setup():
    pass

@contextlib.contextmanager
def working_directory(path):
    prev_cwd = pathlib.Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)

#endregion
#endregion
#endregion
#region path setup
#region Pre Production Setup

pre_prod_dir_names = {
    'Storyboards',
    'Animatics',
    'Color_Scripts',
}

def init_pre_production(path):
    repo_root = pathlib.Path(REPO_ROOT)/path
    pre_pro_root = pathlib.Path(repo_root)/'Pre_Production'
    
    create_dir_if_not_present(pre_pro_root)
    add_readme_file_to_dir(pre_pro_root)
    add_to_dict_and_arr('G_PRE_PRODUCTION',pre_pro_root)

    # sub
    pre_sub_list = create_dirs_from_list(pre_pro_root,pre_prod_dir_names)
    add_files_to_empty_folders(pre_sub_list)

#endregion
#region HSITE setup

hsite_names = [
    'houdini18',
    'houdini19',
]

def hsite_setup():
    #global REPO_ROOT, PROJECT_ROOT
    hsite_root = pathlib.Path(env_dict['PROJECT_ROOT'])/'hsite'
    create_dir_if_not_present(hsite_root)
    add_readme_file_to_dir(hsite_root)
    add_to_dict_and_arr('HSITE',hsite_root)
    hsite_185 = pathlib.Path(hsite_root)/'houdini18.5'
    create_dir_if_not_present(hsite_185)
    add_to_dict_and_arr('HSITE_185',hsite_185)

#endregion
#region Research and Development Setup

def re_and_de_setup():
    global PROJECT_ROOT
    path = pathlib.Path(PROJECT_ROOT)/'Research_and_Development'
    create_dir_if_not_present(path)
    add_readme_file_to_dir(path)

#endregion
#region Post Production Setup

def init_post_production():

    proj_root = pathlib.Path(REPO_ROOT)/'Main_Project'

    # create post production folder
    post_prod_path = pathlib.Path(proj_root)/'Post_Production'
    create_dir_if_not_present(post_prod_path)
    add_readme_file_to_dir(post_prod_path)
    add_to_dict_and_arr('G_POST_PRODUCTION',post_prod_path)

    # Config Global Post Production subdirs
    g_post_subdirlist = create_dirs_from_list(post_prod_path,global_post_dir_namelist)
    #add_files_to_empty_folders(g_post_subdirlist)

    post_proj = Path(post_prod_path)/'Project_Files'
    create_dir_if_not_present(post_proj)
    add_readme_file_to_dir(post_proj)
    post_proj_dirs = create_dirs_from_list(post_proj,post_app_list)
    add_files_to_empty_folders(post_proj_dirs)

    # child dirs
    # audio
    aud_dir = Path(post_prod_path)/'Audio'
    create_dir_if_not_present(aud_dir)
    add_readme_file_to_dir(aud_dir)
    aud_dirs = create_dirs_from_list(aud_dir,post_audio_dir_namelist)
    add_files_to_empty_folders(aud_dirs)
    #sub
    aud_proj = Path(aud_dir)/'Project_Files'
    create_dir_if_not_present(aud_proj)
    add_readme_file_to_dir(aud_proj)
    aud_proj_dirs = create_dirs_from_list(aud_proj, audio_app_list)
    add_files_to_empty_folders(aud_proj_dirs)

    #comp
    comp_dir = Path(post_prod_path)/'Compositing'
    create_dir_if_not_present(comp_dir)
    add_readme_file_to_dir(comp_dir)
    comp_dirs = create_dirs_from_list(comp_dir,post_comp_dir_namelist)
    add_files_to_empty_folders(comp_dirs)
    #sub
    comp_proj = Path(comp_dir)/'Project_Files'
    create_dir_if_not_present(comp_proj)
    add_readme_file_to_dir(comp_proj)
    comp_proj_dirs = create_dirs_from_list(comp_proj,comp_app_list)
    add_files_to_empty_folders(comp_proj_dirs)

    #tex
    tex_dir = Path(post_prod_path)/'Texture'
    create_dir_if_not_present(tex_dir)
    add_readme_file_to_dir(tex_dir)
    tex_dirs = create_dirs_from_list(tex_dir,post_tex_dir_namelist)
    add_files_to_empty_folders(tex_dirs)

    #proj
    tex_proj = Path(tex_dir)/'Project_Files'
    create_dir_if_not_present(tex_proj)
    add_readme_file_to_dir(tex_proj)
    tex_proj_dirs = create_dirs_from_list(tex_proj,tex_app_list)
    add_files_to_empty_folders(tex_proj_dirs)

    #full_dirlist = dir
    add_files_to_empty_folders(g_post_subdirlist)

def init_asset_post_production(path):
    post_prod_path = path
    # ++++++++++

    g_asset_post_subdir_list = create_dirs_from_list(post_prod_path,global_asset_post_dir_namelist)
    
    #general project files
    post_proj = Path(post_prod_path)/'Project_Files'
    create_dir_if_not_present(post_proj)
    add_readme_file_to_dir(post_proj)
    post_proj_dirs = create_dirs_from_list(post_proj,post_app_list)
    add_files_to_empty_folders(post_proj_dirs)

    # audio
    aud_dir = Path(post_prod_path)/'Audio'
    create_dir_if_not_present(aud_dir)
    add_readme_file_to_dir(aud_dir)
    aud_dirs = create_dirs_from_list(aud_dir,post_audio_dir_namelist)
    add_files_to_empty_folders(aud_dirs)
    #sub
    aud_proj = Path(aud_dir)/'Project_Files'
    create_dir_if_not_present(aud_proj)
    add_readme_file_to_dir(aud_proj)
    aud_proj_dirs = create_dirs_from_list(aud_proj, audio_app_list)
    add_files_to_empty_folders(aud_proj_dirs)

    #comp
    comp_dir = Path(post_prod_path)/'Compositing'
    create_dir_if_not_present(comp_dir)
    add_readme_file_to_dir(comp_dir)
    comp_dirs = create_dirs_from_list(comp_dir,post_comp_dir_namelist)
    add_files_to_empty_folders(comp_dirs)
    #sub
    comp_proj = Path(comp_dir)/'Project_Files'
    create_dir_if_not_present(comp_proj)
    add_readme_file_to_dir(comp_proj)
    comp_proj_dirs = create_dirs_from_list(comp_proj,comp_app_list)
    add_files_to_empty_folders(comp_proj_dirs)

    #tex
    tex_dir = Path(post_prod_path)/'Texture'
    create_dir_if_not_present(tex_dir)
    add_readme_file_to_dir(tex_dir)
    tex_dirs = create_dirs_from_list(tex_dir,post_tex_dir_namelist)
    add_files_to_empty_folders(tex_dirs)

    #proj
    tex_proj = Path(tex_dir)/'Project_Files'
    create_dir_if_not_present(tex_proj)
    add_readme_file_to_dir(tex_proj)
    tex_proj_dirs = create_dirs_from_list(tex_proj,tex_app_list)
    add_files_to_empty_folders(tex_proj_dirs)


    add_files_to_empty_folders(g_asset_post_subdir_list)    

#endregion
#region Initialize
#region Choose Project Dir

def choose_proj_dir():
    global env_dict
    proj_name = env_dict['PROJECT_NAME']
    print(proj_name)
    #global PROJECT_ROOT
    if(y_n_q('Do you want to use the current directory?')):
        #PROJECT_ROOT = pathlib.Path(__file__)
        new_path = pathlib.Path(application_path)/proj_name
        PROJECT_ROOT = new_path
        add_var_to_dict('PROJECT_ROOT',new_path)

    else:
        while True:
            try:
                user_input = input('Please type in desired path: ').lower()
                input('Please note the name you chose will be appended to end of the path you set...')
                new_path = pathlib.Path(user_input)/proj_name
                print(new_path.is_dir())
                if new_path.is_dir():
                    if(y_n_q(f'Is {str(new_path)} the correct path?')):
                        add_var_to_dict('PROJECT_ROOT',new_path)
                        print(env_dict['PROJECT_ROOT'])
                        #PROJECT_ROOT = new_path
                        break
                    else:
                        continue
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                print('Directory is not valid! Please try again...')
                continue
    print(f'You have chosen {PROJECT_ROOT} as your main project directory')
    input('Press Enter to continue...')

#region check for projects

#TODO show existing paths
def check_for_existing_projects():
    path = pathlib.Path(application_path)/'.temp.env'
    while True:
        try:
            if(path.is_file()):
                read_temp_file(path)
                break
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print('Creating proj data file...')
            open(path,'a').close()
            continue

def read_temp_file(path):
    with open(str(path), "r+") as help_file:
        contents = help_file.read()
        print(contents)

    help_file.close()

def clear_temp_file():
    path = pathlib.Path(application_path)/'.temp.env'
    if path.is_file():
        path.unlink()

def add_line_to_temp(content):
    #print(f'content: {content}')
    '''
    if file is empty write
    if it is not, check each line,
    if there are duplicates don't write
    '''
    path = pathlib.Path(application_path)/'.temp.env'
    if not path.stat().st_size == 0:
        with path.open("r") as f2:
            lineset = set(f2)
            
        with path.open('w') as f2:
            with path.open('r') as f1:
                for line in f1:
                    if not line in lineset:
                        f2.write(content)
    else:
        with path.open("w") as f:
            f.write(content)


def check_if_line_exists_in_file():
    pass

def check_if_temp_exists():
    path = pathlib.Path(application_path)/'.temp.env'
    if not path.is_file():
        path.open('a').close()

def write_temp(d):
    check_if_temp_exists()
    '''
    incomming dict must be converted from pathlib to string first
    '''
    for k, v in d.items():
        l = str('%s="%s"\n' % (k, v))
        add_line_to_temp(l)



def check_for_projects_in_folder(path):
    result = {}

    inner_proj_dirs = [
        ".config",
        "assets",
        "hsite",
        "packages",
        "Pre_Production",
        "Shots",
    ]

    for p in path.iterdir():
        # print(p)
        curr_dir = p
        subdir_list = []
        try:
            for j in p.iterdir():
                # print(j)
                # curr_dir = j
                for name in inner_proj_dirs:
                    if j.name == name:
                        # print(j)
                        subdir_list.append(j.name)
                        #result[p.name]=p
                subdir_list.sort()
                inner_proj_dirs.sort()
                if(subdir_list == inner_proj_dirs):
                    # print(f'Project:: {curr_dir}')
                    result[p.name]=p
                    #print(p)
        except NotADirectoryError:
            continue
    if len(result)==0:
        print('No projects in directory...')
    else:
        pprint(f'Project folders:: {result}')
        return result

# GUI? #read text file list? terminal input?
from tkinter import filedialog
from tkinter import *

def choose_dir_gui():
    root = tk.Tk()
    root.withdraw()
    folder_selected = tk.filedialog.askdirectory()
    folder_path = pathlib.Path(folder_selected)
    return folder_path

def read_text_list_of_dirs():
    pass

def type_path_of_dir():
    result = input('Please type path of directory to scan: ')
    p = pathlib.Path(result)
    #2print(type(p))
    while True:
        try:
            if p.is_dir():
                print(f'{p} is a directory!')
                break
            else:
                raise NotADirectoryError
        except NotADirectoryError:
            print(f'{p} is not a directory...')
            continue
    return p

#TODO scan or open existing projects
# if no temp or temp is empty bring up below options
# otherwise ask to open currently cached projects or do the below

def user_choose_folder_methods():
    options = {
        1:'default: Scan current directory',
        2:'type in path to scan',
        3:'open gui choose path to scan'
    }
    op_nums = []
    choice = 0
    for k, v in options.items():
        print(f'{k} : {v}')
        op_nums.append(k)

    while True:
        try:
            user_input = int(input('select a number to choose one of the options: '))

            if user_input in op_nums:
                print(f'You chose: {options[user_input]}')
                if user_input == 1:
                    choice = user_input
                elif user_input == 2:
                    choice = user_input
                elif user_input == 3:
                    choice = user_input
                else:
                    raise ValueError
                break
            else:
                raise ValueError
        except ValueError:
            print('Please enter a valid choice...')
            continue
    #print(choice)
    return choice

def choose_folder_method(choice):
    app_root = pathlib.Path(application_path)
    result = ''
    try:
        if choice == 1:
            result = app_root
        elif choice == 2:
            result = type_path_of_dir()
        elif choice == 3:
            result = choose_dir_gui()
        else:
            raise ValueError
    except ValueError:
        print('couldn\'t choose scan method quitting...')
        quit()
    return result

def choose_scan_method(choice):
    app_root = pathlib.Path(application_path)
    result = {}
    try:
        if choice == 1:
            result = check_for_projects_in_folder(app_root)
        elif choice == 2:
            result = check_for_projects_in_folder(type_path_of_dir())
        elif choice == 3:
            result = check_for_projects_in_folder(choose_dir_gui())
        else:
            raise ValueError
    except ValueError:
        print('couldn\'t choose scan method quitting...')
        quit()
    return result

def check_for_project_init():
    pass

def list_projects(env_path):
    temp_file = lib.dotenv.dotenv_values(env_path)
    dotenvdict = dict(unpack_dotenv(temp_file))
    return dotenvdict

def choose_project(p_dict):
    amount = 0
    choice_list = []
    key_list = []
    for k,v in p_dict.items():
        amount+=1
        k_pair = (amount,k)
        key_list.append(k_pair)
        choice_list.append(amount)
    values = p_dict.values()
    values_list = list(values)
    keys = p_dict.keys()
    keys_list = list(keys)
    # print(values_list)
    # print(keys_list)
    print(amount)
    while True:
        try:
            choice = int(input('Please type a corresponding number to open desired project: '))
            if choice in choice_list:
                f_choice = choice - 1
                #get_choice = key_list[0]
                #print(get_choice)
                get_name = keys_list[f_choice]
                get_path = values_list[f_choice]
                #print(f'You chose: {p_dict[]}')
                project_data = (get_name,get_path)
                print(project_data)
                
                break
        except ValueError:
            print('please try again with a valid input...')
            continue


#region ARGPARSE
# create parser
#TODO let user choose default behavior with args
parser = argparse.ArgumentParser()

# add args to parser
# project choose args
parser.add_argument('-pn','--path-project',dest='path_project',action="extend",nargs=1,help='create new project at input path')
parser.add_argument('-un','--gui-project',dest='gui_project',nargs='?',help='create new project at location with gui ')
parser.add_argument('-cn','--current-dir-project',dest='current_dir_project',nargs='?',help='create new project at current path')
parser.add_argument('-pl','--list-projects',dest='list_projects',nargs='?',help='List currently cached projects')
parser.add_argument('-rs','--rescan-folders',dest='rescan_dirs',nargs='?',help='rescan cached directories')
parser.add_argument('-cp','--clear-project-cache',dest='clear_cache',nargs='?',help='clear project cache')


# per project args
parser.add_argument('-i','--init',dest='init', nargs='?',help='Forces initialization')
parser.add_argument('-I','--init-only',dest='init_only', nargs='?',help='Forces ONLY the initialization step')
parser.add_argument('-l','--load-last',dest='load_last', nargs='?',help='Load last opened file')
parser.add_argument('-?','--info',dest='info', nargs='?',help='Shows another help file')


# parse the args
args = parser.parse_args()
#endregion
#region project init main

# CLI 
# -p - input path to scan directories
# -u - use GUI to choose path
# -lp - list cached projects
# -rs - rescan saved directories for project


#!!! Per project config
# so we need to choose the project
# default behavior -> once initialized open last project

def projects_init_main():
    # args
    
    temp_dict = {}
    app_root = pathlib.Path(application_path)
    temp_path = pathlib.Path(application_path)/'.temp.env'
    # check if
    #if args.init:
    if not (temp_path.exists()):
        print('First time setup')
        choice = user_choose_folder_methods()
        p_list = choose_scan_method(choice)
        write_temp(p_list)
    else:
        print('The following projects exist...')
        read_temp_file(temp_path)
        if y_n_q('Would you like to open an existing project?'):
            project_list = list_projects(temp_path)
            pprint(project_list)
            choose_project(project_list)
        else:
            print('Create new project')
            print('Choose directory to create project in...')
            choose_folder = user_choose_folder_methods()
            parent_path = choose_folder_method(choose_folder)
            print(parent_path)
            #project_name_setup()



    #print(p_list)
    # p_list = check_for_projects_in_folder(app_root)
    # str_list = convert_env_dict_to_string(p_list)




#endregion
#endregion
#region Project name

def check_for_space_in_string(s):
    result = 0
    for a in s:
        if (a.isspace()==True):
            result += 1
    return result

def set_project_name():
    user_confirm = True
    user_choice = ''
    while True:
        try:
            user_choice = input('Please enter the name of the project: ').lower()
            if(check_for_space_in_string(user_choice)>0):
                print('White space characters not allowed...')
                raise ValueError
            else:
                while user_confirm:
                    try:
                        if y_n_q(f'Is {user_choice} correct?'):
                            user_confirm = False
                        else:
                            raise ValueError
                    except ValueError:
                        continue
            if(user_confirm == False):
                break
            else:
                raise ValueError
        except ValueError:
            print('Please enter a valid choice...')
            continue
    return user_choice

def project_name_setup():
    global PROJECT_NAME
    name = set_project_name()
    PROJECT_NAME = name
    add_var_to_dict('PROJECT_NAME',name)

#endregion
#endregion
#region CLI stuff


#endregion
##############################################
############## Get Initialized ###############
##############################################

def get_initial_paths():
    global env_dict
    global HOUDINI_TERM
    global CONFIG
    global HOME
    global HOU_ROOT
    #global PROJECT_ROOT
    global ASSETS_GLOBAL_ROOT
    global SHOTS_ROOT
    #TODO add option to set project root at cwd?
    new_folders = []
    # config stuff
    CONFIG = create_config_dir()

    # HSITE stuff
    hsite_setup()

    #region logging setup
    #TODO implement log file
    # logfile = pathlib.Path(CONFIG)/'std.log'
    # logging.basicConfig(str(logfile),format='%(asctime)s %(message)s', filemode='w')
    # logger=logging.getLogger()
    # logger.setLevel(logging.DEBUG)
    # logger.debug('test log')
    
    #region

    # TODO: research and development init

    # houdini term
    HOUDINI_TERM = source_houdini()
    add_to_dict_and_arr('HOUDINI_TERM',HOUDINI_TERM)

    #print(CONFIG)
    add_to_dict_and_arr('CONFIG',CONFIG)

    # ACES and 3Delight
    delight_setup()
    aces_check()
    
    # System Pathts
    add_to_dict_and_arr("HOME",HOME)

    # Houdini Root Dir
    hou_root_str = getHouRoot()
    hou_root_path = pathlib.Path(hou_root_str)
    HOU_ROOT = hou_root_path
    add_to_dict_and_arr("HOU_ROOT",HOU_ROOT)
    
    # Repo Root 
    add_to_dict_and_arr("REPO_ROOT",REPO_ROOT)
    
    # Project Root
    #print(env_dict['PROJECT_ROOT'])
    PROJECT_ROOT = env_dict['PROJECT_ROOT']
    create_dir_if_not_present(PROJECT_ROOT)
    # allready added to env   
    #add_to_dict_and_arr("PROJECT_ROOT",PROJECT_ROOT)

    #persistent config
    pers_config_dir = pathlib.Path(PROJECT_ROOT)/'.config'
    PROJECT_CONFIG = create_dir_if_not_present(pers_config_dir)
    add_to_dict_and_arr('PROJECT_CONFIG',pers_config_dir)

    # r and d
    re_and_de_setup()

    # User stuff
    user_init(pers_config_dir)


    # Global Assets Root
    create_dir_if_not_present(pathlib.Path(PROJECT_ROOT,"assets"))
    ASSETS_GLOBAL_ROOT = pathlib.Path(PROJECT_ROOT,"assets")
    add_readme_file_to_dir(ASSETS_GLOBAL_ROOT)
    add_to_dict_and_arr("ASSETS_GLOBAL_ROOT",ASSETS_GLOBAL_ROOT)
    ########## GLOB CHILD DIRS #############


    global_asset_child_dir_list = create_dirs_from_list(ASSETS_GLOBAL_ROOT,global_asset_child_dir_namelist)
    #print(global_asset_child_dir_list)
    #
    add_dirlist_to_dict(global_asset_child_dir_list,"G_")
    #print(env_dict)


    srcrootpath = pathlib.Path(ASSETS_GLOBAL_ROOT)/'SRC'
    global_src_dir_list = create_dirs_from_list(srcrootpath,global_src_dir_namelist)
    add_readme_file_to_dir(srcrootpath)
    add_files_to_empty_folders(global_src_dir_list)
    add_dirlist_to_dict(global_src_dir_list,'G_SRC_')

    georootpath = pathlib.Path(ASSETS_GLOBAL_ROOT)/'GEO'
    global_geo_dir_list = create_dirs_from_list(georootpath,global_geo_dir_namelist)
    add_readme_file_to_dir(georootpath)
    add_files_to_empty_folders(global_geo_dir_list)
    add_dirlist_to_dict(global_geo_dir_list,'G_GEO_')


    texrootpath = pathlib.Path(ASSETS_GLOBAL_ROOT)/'TEXTURE'
    global_tex_dir_list = create_dirs_from_list(texrootpath,global_tex_dir_namelist)
    add_readme_file_to_dir(texrootpath)
    add_files_to_empty_folders(global_tex_dir_list)

    add_dirlist_to_dict(global_tex_dir_list,'G_TEX_')

    #Post Production stuff
    postrootpath = pathlib.Path(ASSETS_GLOBAL_ROOT)/'POST_PRODUCTION'
    global_post_asset_dir_list = create_dirs_from_list(postrootpath,global_asset_post_dir_namelist)
    add_readme_file_to_dir(postrootpath)

    #add setup here
    init_asset_post_production(postrootpath)


    #empty files to empty folders global assets
    add_files_to_empty_folders(global_asset_child_dir_list)

    # PACKAGES
    PACKAGES = pathlib.Path(PROJECT_ROOT,"packages")
    create_dir_if_not_present(PACKAGES)
    add_readme_file_to_dir(PACKAGES)
    add_to_dict_and_arr("PACKAGES",PACKAGES)

    # SHOT ROOT
    SHOTS_ROOT = pathlib.Path(PROJECT_ROOT,"Shots")
    create_dir_if_not_present(SHOTS_ROOT)
    add_readme_file_to_dir(SHOTS_ROOT)
    add_to_dict_and_arr("SHOTS_ROOT",SHOTS_ROOT)
    
    #pre prod
    init_pre_production(PROJECT_ROOT)

    init_post_production()
    #createShotDir(SHOTS_ROOT)

    add_to_dict_and_arr('INITIALIZED','TRUE')

#endregion
#endregion
#region EXECUTE
#region exec helpers
# def parse_dotenv(dotenv_path): 
#     with open(dotenv_path) as f: 
#         for line in f: 
#             line = line.strip() 
#             if not line or line.startswith('#') or '=' not in line: 
#                 continue 
#             k, v = line.split('=', 1) 

#             # Remove any leading and trailing spaces in key, value 
#             k, v = k.strip(), v.strip().encode('unicode-escape').decode('ascii') 

#             if len(v) > 0:
#                 quoted = v[0] == v[len(v) - 1] in ['"', "'"] 

#                 if quoted: 
#                     v = decode_escaped(v[1:-1]) 

#             yield k, v



def check_init(env_path) -> bool:
    global env_dict
    input(f'ENV PATH::: {env_path}')
    result = False
    config = ''
    if(env_path.is_file()):
        config = dotenv_values(env_path)
        env_dict = config
        #pprint(config)
        result = True
    else:
        result = False
    return result

# def unpack(data):
#     for k, v in data.items():
#         if isinstance(v, dict):
#             yield from unpack(v)
#         else:
#             yield v

# def depth(it, count=0):
#     """Depth of a nested dict.
#     # Arguments
#         it: a nested dict or list.
#         count: a constant value used in internal calculations.
#     # Returns
#         Numeric value.
#     """
#     if isinstance(it, list):
#         if any(isinstance(v, list) or isinstance(v, dict) for v in it):
#             for v in it:
#                 if isinstance(v, list) or isinstance(v, dict):
#                     return depth(v, count + 1)
#         else:
#             return count
#     elif isinstance(it, dict):
#         if any(isinstance(v, list) or isinstance(v, dict) for v in it.values()):
#             for v in it.values():
#                 if isinstance(v, list) or isinstance(v, dict):
#                     return depth(v, count + 1)
#         else:
#             return count
#     else:
#         return count





#endregion
#endregion
#region MAIN
def main(project_data):
    # global env_dict
    global parser

    #projects_init_main()
    # fix app dir for compile
    #env_path = pathlib.Path()/'.config/config.env'
    # CLI stuff
    # switches = [i for i in sys.argv if re.match(r'^-[A-Za-z]+$',i)]
    # args_kwargs = [i for i in sys.argv if not re.match(r'^-[A-Za-z]+$', i)]
    # cli_check(switches,args_kwargs)
    #print(f'root dir:: {pathlib.Path.root}')
    # get the arguments value
    if args.init:

        print('Forcing Initialization')
        # 3rd party software
        #project_name_setup()
        choose_proj_dir()

        indie_check()
        redshift_main()
        # initialize
        get_initial_paths()
        # Shot stuff
        shot_decision()
        #houdini setup
        houdini_file_main()
        # config files
        
        create_config_files(env_dict)
        # open houdini
        houdini_main()
    elif args.init_only:

        print('Forcing Initialization, not opening Houdini...')
        #project_name_setup()
        choose_proj_dir()
        # 3rd party software
        indie_check()
        redshift_main()
        # initialize
        get_initial_paths()
        # Shot stuff
        shot_decision()
        #houdini setup
        houdini_file_main()
        # config files
        create_config_files(env_dict)

    elif args.load_last:

        print('Loading last opened file')
        env_vars = env_from_file(env_path)
        #result = [list(unpack(x)) for x in env_vars]
        #result = depth(env_vars,1)
        #TODO use flatdict in houdini setup
        result = dict(unpack_dotenv(env_vars))
        
        add_dict_to_dict(result,env_dict)
        
        #pprint(result)
        houdini_main()
    elif args.info:
    
        # from rich.console import Console
        # from rich.markdown import Markdown
        # print('man page')
        f = pathlib.Path(pathlib.Path.cwd())/'app/doc/info.md'
        with open(str(f), "r+") as help_file:
            #Console.print(help_file,soft_wrap=True)
            contents = help_file.read()
            print(contents)
            # Console.push_render_hook(Console,RENDER)
            # Console.print(contents,soft_wrap=True)
            # Console.pop_render_hook()
        help_file.close()
        quit()
    else:
        if not (check_init(env_path)):

            choose_proj_dir()
            # 3rd party software
            indie_check()
            redshift_main()
            # initialize
            get_initial_paths()
            # Shot stuff
            shot_decision()
            #houdini setup
            houdini_file_main()
            # config files
            create_config_files(env_dict)
            # open houdini
            houdini_main()

        else:
            
            env_vars = env_from_file(env_path)
            #result = [list(unpack(x)) for x in env_vars]
            #result = depth(env_vars,1)
            #TODO use flatdict in houdini setup
            dotenvdict = dict(unpack_dotenv(env_vars))
            
            add_dict_to_dict(dotenvdict,env_dict)
            
            #pprint(env_dict)

            # Shot stuff
            shot_decision()
            #houdini setup
            houdini_file_main()
            # config files
            create_config_files(env_dict)
            # open houdini
            houdini_main()


if __name__ == "__main__":
    projects_init_main()
    main()
    #pass

#endregion
#endregion
