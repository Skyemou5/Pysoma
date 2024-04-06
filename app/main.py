#!/usr/bin/python3
#region HEADER

import argparse
import glob
import json
import os
import pathlib
import pprint
import re
import shutil
import sys
import sqlite3
#import tk
import tkinter as tk
from pathlib import Path, PurePath

#####################################################
#####################################################
#####################################################


from pprint import pprint
from pydoc import resolve
from sqlite3 import DataError
from sys import platform, stderr, stdout
# from telnetlib import EXOPL
from textwrap import indent
from turtle import up
from typing import OrderedDict
from unicodedata import name

import dotenv
import dump_env
import ruamel.yaml
from ruamel.yaml import YAML, yaml_object
from yamlize import Object

#import lib.flatdict as flatdict
import flatdict

import pysoma_lib as plib
##############################################
##############################################
##############################################
#endregion
#region VARIABLES

#######################################
################ VARS #################
#######################################

######## Default Hou paths #########
# Linux houdini_setup_bash         #
# mac houdini terminal             #
# win houdini command line tools   #
####################################
yaml = YAML()




#endregion
#region fix compile issues
if getattr(sys, 'frozen', False):
    import os
    import sys

    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))



#endregion

# fixing yaml dumping with aliases
class NonAliasingRTRepresenter(ruamel.yaml.representer.RoundTripRepresenter):
    def ignore_aliases(self, data):
        return True



#yaml.representer = NonAliasingRTRepresenter

hip_file_ext = [
    'hip',
    'hipnc',
    'hiplc',
]

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
    #add_var_to_dict('HOUDINI_DSO_ERROR',str(2))
    rs_key = 'RS_PATH'
    #add_var_to_dict(rs_key,redshift_paths[platform])
    rs_path = pathlib.Path(redshift_paths[platform])
    #add_var_to_dict('USE_RS',str(1))
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
        #add_var_to_dict('USE_RS',str(0))
        return False
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


def load_from_config(dotenv_file):
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

    env_dict_file = dotenv.dotenv_values(env_file)
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

#endregion
#endregion
#endregion
#region Projects Main
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
                        if plib.y_n_q(f'Is {user_choice} correct?'):
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

#endregion

# #region ARGPARSE

# #TODO impliment multicommand as nested library

import multicommand


class _HelpAction(argparse._HelpAction):

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        child_parsers = [
            #action for action in parser.
        ]
        # retrieve subparsers from parser
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)
            ]
        
        # there will probably only be one subparser_action,
        # but better save than sorry
        for subparsers_action in subparsers_actions:
            
            # get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                
                print("Subparser '{}'".format(choice))
                print(subparser.format_help())

        parser.exit()
double_line = '==================================================================================================='

# create the top-level parser
parser = argparse.ArgumentParser(
    prog='Pysoma', 
    conflict_handler='resolve',
    usage='%(prog)s [options]',
    description='-------------------------PYSOMA-------------------------',
    epilog=double_line
    )  # here we turn off default help action
subparsers = parser.add_subparsers(help="Commands",dest='command')

parser.add_argument('-h','--help', action=_HelpAction, help='help for help if you need some help')  # add custom help
parser.add_argument('--version', action='version', version='1.0.0')
#TODO impliment --verbose

# info parser
info_parser = subparsers.add_parser(
    'info',
    help='display helpful information about the app and projects',
    description='--------------------Useful info about app and projects--------------------',
    epilog=double_line
    )
info_group = info_parser.add_argument_group('info')
info_args_group = info_group.add_mutually_exclusive_group()
info_args_group.add_argument('-d','--documentation',dest='documentation', action='store_true',help='opens documentation - TODO')
info_args_group.add_argument('-c','--config',dest='config', action='store_true',help='prints paths of config files')


# config parser
# TODO database stuff

config_parser = subparsers.add_parser(
    'config',
    help='manage app and project configuration',
    description='--------------------Manage configuration--------------------',
    epilog=double_line
    )
config_group = config_parser.add_argument_group('config')
config_args_group = config_group.add_mutually_exclusive_group()
config_args_group.add_argument('-lp','--list-projects',dest='list_projects',choices=['names','more','path'],help='List currently cached projects')
config_args_group.add_argument('-rs','--rescan-folders',dest='rescan_dirs',action='store_true',help='rescan cached directories')
config_args_group.add_argument('-cp','--clear-project-cache',dest='clear_cache',action='store_true',help='clear project cache')
config_args_group.add_argument('-tll','--toggle-load-last',dest='toggle_load_last', action='store_true',help='toggle load-last config')
config_args_group.add_argument('-I','--init-only',dest='init_only' ,action='store_true',help='Forces ONLY the initialization step')
config_args_group.add_argument('-i','--init',dest='init',action='store_true',help='Forces initialization')
config_args_group.add_argument('-dp','--default-project', dest='default_project', action='store_true',help='sets the default project to open')
config_args_group.add_argument('-pp','--prune-projects', dest='prune_projects', action='store_true',help='checks saved projects to see if they exist and removes them if they don\'t')
config_args_group.add_argument('-mp','--move-projects', dest='move_projects', nargs='+',help='Moves named projects to new root path. !This will break you\'re project if you aren\'t using env vars and relative paths!')

# project_config=parser = subparsers.add_parser(
#     'project-config',
#     help='manage app and project configuration',
#     description='--------------------Manage configuration--------------------',
#     epilog=double_line

# )


# create project parser
create_project_parser = subparsers.add_parser(
    'create-projects',
    help='Create new project(s)',
    description='--------------------Create new project(s) that don\'t exists yet--------------------',
    epilog=double_line
)
create_project_group = create_project_parser.add_argument_group('Create Project(s)')
create_project_args_group = create_project_group.add_mutually_exclusive_group()
#TODO add support for a file of list of names or CSV
create_project_args_group.add_argument('-p','--path',dest='path_project',action="extend",nargs='+',help='add project at input path(s), then include names of new projects to add to folder')
create_project_args_group.add_argument('-g','--create_gui-project',dest='gui_project',action='store_true',help='create new project at location with gui ')
create_project_args_group.add_argument('-cwd','--craete-cwd-project',dest='cwd_project',nargs='+',help='create new project at current working directory')



# add project parser
add_project_parser = subparsers.add_parser(
    'add-projects',
    help='Add new project(s)',
    description='--------------------Add project(s) that already exists--------------------',
    epilog=double_line
    )
add_project_group = add_project_parser.add_argument_group('Add Project(s)')
add_project_args_group = add_project_group.add_mutually_exclusive_group()
add_project_args_group.add_argument('-p','--path',dest='path_project',action="extend",nargs='+',help='add project at input path(s)')
add_project_args_group.add_argument('-ui','--add_gui-project',dest='gui_project',action='store_true',help='create new project at location with gui ')
add_project_args_group.add_argument('-cn','--add_current-dir-project',dest='current_dir_project',action='store_true',help='create new project at current path')



# Open Project parser
open_project_parser = subparsers.add_parser(
    'open-project',
    help='Open existing project',
    description='--------------------Open a project saved in config--------------------',
    epilog=double_line
    )
open_project_group = open_project_parser.add_argument_group('Open Project')
open_project_args_group = open_project_group.add_mutually_exclusive_group()
open_project_args_group.add_argument('-n','--by-name',dest='by_name', nargs=1, help='opens project by name')
open_project_args_group.add_argument('-l','--load-last',dest='load_last', action='store_true', help='Load last opened file')
open_project_args_group.add_argument('-pl','--open-project-list', dest='open_project_list', action='store_true',help='load project from list of projects')


# shot parser
shot_parser = subparsers.add_parser(
    'shots',
    help='open or create shot folders',
    description='--------------------Open Or create shots in a project--------------------',
    epilog=double_line
)
shot_group = shot_parser.add_argument_group('shot')
shot_args_group = shot_group.add_mutually_exclusive_group()
shot_args_group.add_argument('-os','--open-shot',dest='open_shot', nargs='?',help='open shot for project')
shot_args_group.add_argument('-cs','--create-n-shots',dest='create_shots',nargs=1, type=int,help='create any number of shots')



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
main_config = plib.MainConfig()
# TODO:convert to yaml from config
def projects_init_main() -> tuple:
    # args

    def create_project(name=None,root_path=None) -> plib.ConfigData:

        print('Creating a new project...')
        main_config.data['None']['appdata']['initialized']=True
        if name is None:
            project_name = set_project_name()
        else:
            project_name = name
        
        project_data = plib.ProjectData()
        project_data.name = project_name

        if root_path is None:
            choice = plib.user_choose_folder_methods_noscan()
            path = plib.choose_folder_method(choice)
        else:
            path = root_path
        
        project_data.parent_path = pathlib.Path(path)

        project_path = pathlib.Path(path)/project_data.name

        project_data.path = project_path
        
        new_project = plib.ProjectSetup()
        new_project.create_project(vars(project_data))
        project_data.config = new_project.config_path
        
        project_data.env = new_project.enviornment_variables
        # not fully initialized until shot decision
        project_data.initialized = False
        project_data.project_root = project_path
        project_data.name = project_name
        
        #region Set houdini version


        project_data.houdini_major_version = "19.5"
        project_data.houdini_minor_version = "605"
        print(f'The houdini version is set to {project_data.houdini_major_version}.{project_data.houdini_minor_version}......')
        if plib.y_n_q("Would you like to change the houdini version to use for this project?"):
            houdini_major = input("Please type in the major houdini version. Ex: 18.5: ")
            houdini_minor = input("now the minor version: ex: 759: ")
            project_data.houdini_major_version = houdini_major
            project_data.houdini_minor_version = houdini_minor

        #endregion


        #print("now the minor version: ex: 759")
        project_data.shots = pathlib.Path(project_path)/'shots'

        project_data.houdini_install_path = main_config.get_hou_path(project_data)
        simple_project_data = project_data.main_config_list_data()
        main_config.add_project(simple_project_data)
        
        #pprint(main_config.data)
        new_project_config_data = {}
        new_project_config_data['None']=vars(project_data)
        new_project.create_configs(new_project_config_data)
        new_project.save_templates()
        #pprint(main_config.data)
        #pprint(main_config.config.data)
        main_config.update_and_write_config()

        if name is None and root_path is None:
            # print(project_data.config + "/project_data.yml")
            # print(plib.ConfigData(project_data.config).config_file)
            new_project_config = plib.ConfigData(project_data.config + "/project_data.yml")

            return new_project_config
        # pprint(vars(project_data))
    #TODO add houdini versions and paths if they don't exist. allow user to configure
    def add_existing_project(project_path=None) -> tuple:

        while True:
            
            # if project_path is None:
            project_path = plib.choose_folder_method(plib.user_choose_folder_methods_noscan())
                
            config_path = pathlib.Path(project_path)/'.config/project_data.yml'
            for project in main_config.project_list:
                if project['path'] == str(project_path):
                    print(f'Project <{project["name"]}> already exists!')
                    print('pick another folder or exit...')
                    continue
            try:
                if config_path.exists():
                    project_data = ProjectData()
                    return plib.ConfigData(config_path), project_data.update_from_dict(plib.ConfigData(config_path).data['config'])

                
            except:
                print('not a valid project please choose another folder')
                continue
        #return new_project_config

    def choose_existing_project() -> tuple:

        print('The following projects exist...')
        for i, item in enumerate(main_config.project_list):
            print(f'{i+1} : {item["name"]}')
        choice = plib.choose_project_from_list(main_config.project_list)
        #print(choice)
        chosen_project = main_config.project_list[choice[0]-1]
        #chosen_project['last_opened']=True
        main_config.update_projects()
        main_config.update_config()
        main_config.write_config()
        #print(chosen_project['config'])
        # project_data = ConfigData(pathlib.Path(chosen_project['config'])/'project_data.yml')
        project_data = plib.ProjectData()
        new_project_config = plib.ConfigData(chosen_project['config'])
        #pprint(new_project_config.data)
        #project_data.from_yaml(new_project_config.data)
        project_data.load_from_file(chosen_project['config'])
        #pprint(vars(project_data))

        return new_project_config, project_data
        # pprint(main_config.data)
        # pprint(project_data.data)

    def open_project(project_data: plib.ProjectData):
        #pprint(project_data.data)
        #pprint(main_config.data)
        print(f'Opening project <{project_data.data["None"]["name"]}> .......')
        project_data_obj = plib.ProjectData()
        project_data_obj.update_from_dict(project_data.data)
        main_config.update_last_opened(project_data_obj.main_config_list_data())
        main_config.update_and_write_config()
        # pprint(vars(project_data_obj))
        return project_data

    # def project_choice_action():
    #     print("project choice action")


    #TODO fix project choice
    def user_choice_list(choice_dict:dict) -> plib.ConfigData:
        #
        
        print(f'choice dict: {choice_dict}')
        while True:
            project_choice_action = plib.user_choice_from_list(choice_dict)
            # print(project_choice_action)
            project_choice_data = project_choice_action()
            # pprint(project_choice_data.data)
            if plib.y_n_q(f'Do you want to open <{project_choice_data.data["name"]}>'):
                break
            else:
                continue
        return project_choice_data

    def get_last_opened():

        last_opened_data = main_config.data['None']['appdata']['last_opened']
        project_config_data = plib.ConfigData(last_opened_data['config'])
        project_data = plib.ProjectData()
        project_data.update_from_dict(project_config_data.data)
        #pprint(vars(project_data))
        return project_config_data

    ###########################################
    ################ CLI args #################
    ###########################################

    chosen_project = None
    #print(args.command)
    if args.command is not None:
        # use shlex?
        if args.command == 'info':
            if args.documentation:
                print('TODO - open documentation website')
                exit()
            elif args.config:
                str_app_path = str(application_path)
                print(f'config path={str_app_path}')
                exit()
            else:
                print('short version of help, use -h or --help for long version')
                parser.print_help()
        elif args.command == 'config':

            if args.list_projects:
                if args.list_projects == 'more':
                    print('Currently saved projects...')
                    for i, item in enumerate(main_config.project_list):
                        print(f'{i+1} : <{item["name"]}>')
                        for k,v in item.items():
                            if not k == 'name':
                                print(f'          {k} : {v}')
                    exit()
                elif args.list_projects == 'name':
                    print('Currently saved projects...')
                    for i, item in enumerate(main_config.project_list):
                        print(f'{i+1} : <{item["name"]}>')
                    exit()
                elif args.list_projects == 'path':
                    print('Currently saved projects...')
                    for i, item in enumerate(main_config.project_list):
                        print(f'{i+1} : <{item["path"]}>')
                    exit()


            elif args.rescan_dirs:
                print('TODO - rescanning dirs')

            elif args.clear_cache:
                main_config.project_list = None
                main_config.update_projects()
                main_config.data['None']['appdata']['initialized']=False
                main_config.data['None']['appdata']['open_last']=False
                main_config.update_last_opened(None)
                main_config.update_and_write_config()
                exit()

            elif args.toggle_load_last:
                print('load last toggled....')
                main_config.data['None']['appdata']['open_last'] = not main_config.data['None']['appdata']['open_last']
                main_config.update_and_write_config()
                print(f"load last set to: {main_config.data['None']['appdata']['open_last']}")
                exit()

            elif args.init:
                if plib.y_n_q('Do you want to always open the last opened project by default?'):
                    main_config.config.data['None']['appdata']['open_last']=True
                else:
                    main_config.config.data['None']['appdata']['open_last']=False
                
                main_config.config.data['None']['appdata']['initialized']=True
                main_config.update_and_write_config()

            elif args.init_only:
                main_config.config.data['None']['appdata']['open_last']=False
                main_config.config.data['None']['appdata']['initialized']=False
                main_config.update_and_write_config()
                exit()

            elif args.default_project:
                if main_config.data['None']['projects'] is not None:
                    proj_list = {}
                    for project in main_config.project_list:
                        print(project)
                else:
                    print('There are no projects saved to config!')
                    exit()

            elif args.prune_projects:
                new_project_list = []
                print('the following projects no longer exist...')
                for pr in main_config.project_list:
                    if not pathlib.Path(pr['path']).is_dir():
                        print(f"removed <{pr['name']}> from project list...")
                    else:
                        new_project_list.append(pr)
                main_config.project_list = new_project_list
                main_config.update_projects()
                main_config.update_and_write_config()
                exit()

            elif args.move_projects:
                '''
                Move projects to a new location and update config
                '''
                if len(args.move_projects) <= 1:
                    print('You must specify which projects to move...')
                    exit()
                
                move_project_args = args.move_projects
                root_path = pathlib.Path(move_project_args.pop(0)).resolve()
                projects = move_project_args
                project_list = list(main_config.project_list)
                old_parent_path = pathlib.Path(project_list[0]['path']).parent
                old_project_list = []
                
                # valid_project_names = True
                
                # # check for valid project names
                # # if project names valid - continue
                # for p in project_list:
                #     for n in projects:
                #         if not p['name']==n:
                #             valid_project_names = False
                # if not valid_project_names:
                #     print('no valid projects')
                #     exit()
                
                for i in project_list:
                    old_project_list.append(i)

                if len(project_list) == 0:
                    print('No projects saved')  
                    exit()

                original_project_paths = {}
                updated_project_list = []

                changed_projects = []

                # Update current project list
                for index, item in enumerate(project_list):

                    if item['name'] in projects:
                        item['path']=pathlib.Path(root_path)/item['name']
                        item['config']=pathlib.Path(root_path).joinpath(item['name'])/'.config/project_data.yml'
                        changed_projects.append(project_list[index])

                # pprint(project_list)
                main_config.project_list = project_list

                # pprint(main_config.project_list)
                main_config.update_projects()
                main_config.update_and_write_config()
                new_parent_path = pathlib.Path(changed_projects[0]['path']).parent

                project_paths_dict = {}
                def move_project(new_project_item):
                    old_path = str(pathlib.Path(old_parent_path)/new_project_item['name'])
                    new_path = str(new_project_item['path'])
                    if not pathlib.Path(new_path).exists():
                        try:
                            if new_parent_path.is_dir() and new_parent_path.exists():
                                pass
                            else:
                                raise FileNotFoundError
                        except FileNotFoundError:
                            print('Parent Folder doesn\'t exist, creating folder...')
                            os.makedirs(str(new_parent_path.resolve()))
                            # item['path'].mkdir()
                            # shutil.move(str(oldpath),str(item['path']))
                        finally:
                            print('moving project')
                            shutil.move(old_path,new_path)
                    else:
                        pass
                for item in changed_projects:
                    pprint(item)
                    move_project(item)
                    update_config = ProjectParse(item)
                    update_config.refresh_project_data()
                exit()

        elif args.command == 'create-projects':
            if args.path_project:
                path_project_args = args.path_project
                root_path = pathlib.Path(path_project_args.pop(0))
                print(f'Creating projects in {root_path.absolute()}')
                project_name_list = []
                for pr in main_config.project_list:
                    project_name_list.append(pr['name'])
                
                for i, item in enumerate(path_project_args):
                    p = pathlib.Path(root_path).joinpath(item).resolve()
                    if not p.is_dir():
                        print(f'Creating project <{p.name}> at: {p.absolute()}')
                        create_project(p.name,root_path.absolute())
                    else:
                        print(f'{p.name} is already a directory!')
                        # TODO impliment check for valid projects
                        config_path = pathlib.Path(p)/'.config/project_data.yml'
                        if config_path.is_file():
                            print('and a Valid Project')
                            if item not in project_name_list:
                                print('project not in config')
                                if plib.y_n_q('Do you wish to add it?'):
                                    existing_project_config = plib.ConfigData(config_path)
                                    existing_project_data = plib.ProjectData()
                                    existing_project_data.update_from_dict(existing_project_config.data)
                                    main_config.add_project(existing_project_data.main_config_list_data())
                                    main_config.update_and_write_config()
                        else:
                            if plib.y_n_q('Do you want to create project in folder anyway?'):
                                plib.create_project(p.name,root_path.absolute())
                exit()
            elif args.gui_project:
                project_name = set_project_name()
                path = plib.choose_dir_gui()
                plib.create_project(project_name,path)
                exit()
            elif args.cwd_project:
                path_project_args = args.cwd_project
                root_path = pathlib.Path(application_path)
                print(f'Creating projects in {root_path}')
                project_name_list = []
                for pr in main_config.project_list:
                    project_name_list.append(pr['name'])
                
                for i, item in enumerate(path_project_args):
                    p = pathlib.Path(root_path).joinpath(item).resolve()
                    if not p.is_dir():
                        print(f'Creating project <{p.name}> at: {p.absolute()}')
                        plib.create_project(p.name,root_path.absolute())
                    else:
                        print(f'{p.name} is already a directory!')
                        # TODO impliment check for valid projects
                        config_path = pathlib.Path(p)/'.config/project_data.yml'
                        if config_path.is_file():
                            print('and a Valid Project')
                            if item not in project_name_list:
                                print('project not in config')
                                if plib.y_n_q('Do you wish to add it?'):
                                    existing_project_config = plib.ConfigData(config_path)
                                    existing_project_data = plib.ProjectData()
                                    existing_project_data.update_from_dict(existing_project_config.data)
                                    main_config.add_project(existing_project_data.main_config_list_data())
                                    main_config.update_and_write_config()
                        else:
                            if plib.y_n_q('Do you want to create project in folder anyway?'):
                                plib.create_project(p.name,root_path.absolute())


        elif args.command == 'add-projects':
            if args.path_project:
                for p in args.path_project:
                    while True:
                        try:
                            if p.is_dir():
                                print(f'<{p}> is a directory!')
                                break
                            else:
                                raise NotADirectoryError
                        except NotADirectoryError:
                            print(f'<{p}> is not a directory...')
                            continue
                    #print(args.path_project)
                    
                    plib.add_existing_project(p)
                    # /home/ben/dev/Aces_Stuff/Pysoma/app/tt /home/ben/dev/Aces_Stuff/Pysoma/app/ff

                exit()
            elif args.gui_project:
                print('gui')
                pp = choose_dir_gui()
                plib.add_existing_project(pp)
                exit()
            elif args.current_dir_project:
                print('TODO ---')
                exit()
            else:
                print('please check help and use a correct flag')
                exit()
        elif args.command == 'open-project':
            if args.by_name:
                name = args.by_name[0]
                exists = False
                project_config_data = None
                for project in main_config.project_list:
                    #print(project['name'])
                    #print(f'input name: {name}')
                    if project['name']==str(name):
                        print(f'Project <{name}> exists!')
                        exists = True
                        project_config_data = plib.ConfigData(project['config'])

                if exists:
                    chosen_project = open_project(project_config_data)
                else:
                    print('Project name not recognized...')
                    exit()

            elif args.load_last:
                if main_config.data['None']['appdata']['last_opened'] is not None:
                    project_config_data = plib.ConfigData(main_config.data['None']['appdata']['last_opened']['config'])
                    chosen_project = open_project(project_config_data)
                else:
                    print('No project loaded last...')
                    exit()

            elif args.open_project_list:
                choice = plib.choose_existing_project()
                chosen_project = open_project(choice)

            else:
                exit('please check help and use a correct flag')
        elif args.command == 'shots':
            # pass data to shots
            if main_config.data['None']['appdata']['last_opened'] is not None:
                project_config_data = pl;ib.ConfigData(main_config.data['None']['appdata']['last_opened']['config'])
                chosen_project = open_project(project_config_data)
            else:
                choice = plib.choose_existing_project()
                chosen_project = open_project(choice)

        
            print('open shots')
            return chosen_project
    else:
        print('no-args')


        ###########################################
        ############## No CLI args ################
        ###########################################


        project_choices = {
            'Would you like to open an existing project?':choose_existing_project,
            'Would you like to add an existing project?':add_existing_project,
            'Would you like to create a new project?':create_project,
        }

        initial_project_choices = {
            'Would you like to add an existing project?':add_existing_project,
            'Would you like to create a new project?':create_project,
        }
        
        if not (main_config.config.data['None']['appdata']['initialized']):
            print('First time setup')
            # ask about defaults
            if plib.y_n_q('Do you want to always open the last opened project by default?'):
                main_config.config.data['None']['appdata']['open_last']=True
            else:
                main_config.config.data['None']['appdata']['open_last']=False

            main_config.config.data['None']['appdata']['initialized']=True
            main_config.update_and_write_config()

            # first project stuff
            chosen_project = open_project(user_choice_list(initial_project_choices))

        elif main_config.config.data['None']['appdata']['last_opened'] is not None and main_config.config.data['None']['appdata']['open_last']:

            #print('the following projects no longer exist...')

            if not pathlib.Path(main_config.last_opened['path']).is_dir():
                print('the saved last opened project no longer exists...')
                print(f"removed <{main_config.last_opened['name']}> from project list...")
                main_config.update_last_opened(None)
                if main_config.config.data['None']['projects'] is None:
                    print('There are no projects saved')
                    chosen_project = open_project(user_choice_list(initial_project_choices))
                else:
                    print('There are projects saved in your config')
                    chosen_project = open_project(user_choice_list(project_choices))
                return chosen_project
            else:
                print('opening last opened project')
                chosen_project = open_project(get_last_opened())
        else:
            if main_config.config.data['None']['projects'] is None:
                print('There are no projects saved')
                chosen_project = open_project(user_choice_list(initial_project_choices))
            else:
                print('There are projects saved in your config')
                #TODO: fix this open project thing

                chosen_project = open_project(user_choice_list(project_choices))
        return chosen_project


#TODO implement cleaning project list in config

#endregion
#endregion
#endregion
#endregion
#region Shot Main
#region Houdini file









#endregion
#endregion
#endregion

#endregion
#region MAIN

#TODO fix shot folder creation

def main():
    opened_project = projects_init_main()
    print(opened_project)
    # shot_data = shot_main(opened_project)
    # houdini main

if __name__ == "__main__":
    main()


#endregion
#endregion
