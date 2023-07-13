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
import tkinter as tk
from pathlib import Path, PurePath

#####################################################
#####################################################
#####################################################

from pprint import pprint
from pydoc import resolve
from sqlite3 import DataError
from sys import platform, stderr, stdout
from telnetlib import EXOPL
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



###############################
####### DIRECTORY PATHS #######
###############################


def unpack_dotenv(env_d):
    import lib.flatdict as flatdict
    result = flatdict.FlatDict(env_d,delimiter=':')
    return result


def env_from_file(path):
    #env_file = pathlib.Path(pathlib.Path.cwd())/'.config/config.env'
    dict_var = dotenv_values(path)
    #print(dict_var)
    return dict_var


def is_empty(folder: Path) -> bool:
    return not any(folder.iterdir())

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

### config files

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

# User info
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

# folder helper functions

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

# More helpers

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

def should_remove_line(line,stop_words):
    return any([word in line for word in stop_words])

def overwrite_line(key,content):
    stop_words = key
    path = pathlib.Path(application_path)/'.temp.env'
    if not path.stat().st_size == 0:
        with path.open('r') as f1:
            with path.open('w') as f2:
                for line in f1:
                    if not should_remove_line(line,stop_words):
                        f2.write(line)
    add_line_to_temp(content)

def check_if_temp_empty():
    result = ''
    path = pathlib.Path(application_path)/'.temp.env'
    if path.stat().st_size == 0:
        result = True
    else:
        result = False
    print(f'Temp file is empty: {result}')
    return result

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

def get_level(dct, level):
    if level == 0:
        yield from ((k, v) for k, v in dct.items() if not isinstance(v, dict))
    else:
        yield from ((kk, vv) for v in dct.values() if isinstance(v, dict) for kk, vv in get_level(v, level-1))

def parse_nested_dict(data):
    result = {}
    stack = list(data.items())
    visited = set()
    while stack:
        k, v = stack.pop()
        if isinstance(v,dict):
            if k not in visited:
                stack.extend(v.items())
        else:
            if k == 'name':
                result[k]=v
                #print("%s: %s" % (k,v))
            #self.new_data[k]=v
            #print("%s: %s" % (k,v))
            pass
        visited.add(k)
    return result

def flatten_dict(data):
    import lib.flatdict as flatdict
    result = flatdict.FlatDict(data,delimiter=':')
    return result

def add_project_to_list(path):
    pass

def check_for_projects_in_folder(path):
    # TODO: Fix directory scanning
    
    result = {}

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
                        print(j)
                        subdir_list.append(j.name)
                        result[p.name]=p
                subdir_list.sort()
                inner_proj_dirs.sort()
                if(subdir_list == inner_proj_dirs):
                    print(f'Project:: {curr_dir}')
                    result[p.name]=p
                    print(p)
        except NotADirectoryError:
            continue
    if len(result)==0:
        print('No projects in directory...')
    else:
        pprint(f'Project folders:: {result}')
        return result



# GUI? #read text file list? terminal input?
from tkinter import *
from tkinter import filedialog


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
def user_choose_folder_methods_noscan() -> int:
    options = {
        1:'default: Open gui to choose path',
        2:'type in path to scan',
        3:'Current application directory',
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



def choose_folder_method(choice: int):
    app_root = pathlib.Path(application_path)
    result = ''
    print(f'your choice:: {choice}')
    try:
        if choice == 1:
            print('open gui')
            result = choose_dir_gui()
        elif choice == 2:
            result = type_path_of_dir()
        elif choice == 3:
            result = application_path
        else:
            raise ValueError
    except ValueError:
        print('couldn\'t choose scan method quitting...')
        quit()
    return result

def choose_folder_scan_method(choice):
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
        print('couldn\'t choose folder method method quitting...')
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
    temp_file = dotenv.dotenv_values(env_path)
    dotenvdict = dict(unpack_dotenv(temp_file))
    return dotenvdict


def write_to_second_temp(d_content):
    path = pathlib.Path(application_path)/'.config.env'
    for k, v in d_content.items():
        l = str('%s="%s"\n' % (k, v))
        with path.open('w') as f:
            f.write(l)

#region project setup helpers

def choose_project_from_list(l: list):
    #print(len(l))
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
            result = check_if_num_in_list(choice,l)
            if (result == True):
                proj = l[choice-1]
                proj_name = proj['name']
                print(f'You chose <{proj_name}>')
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


# TODO: replace all list choices with this generalized list choice funtion
def user_choice_from_list(prompts_and_choices):
    '''
    Generalized list choice funtion.
    The input dictionary should have the strings as prompts for each key,
    and the values should be whatever you want to return for each choice
    '''
    try:
        if isinstance(prompts_and_choices, dict):
            counter = 1
            choices_items = list(prompts_and_choices)
            choices_keys = list(prompts_and_choices.keys())
            choices_values = list(prompts_and_choices.values())
            #print(type(choices_items))
            for k,v in prompts_and_choices.items():
                print(f'{counter} : {k}')
                counter += 1
            print('-------------------')
            while True:
                try:
                    choice_first = input(f'Please type a corresponding number for one of the {len(prompts_and_choices)} choices: ')
                    choice = int(choice_first)
                    if check_if_num_in_list(choice,choices_items):

                        if y_n_q(f'Is <{choice}> correct?'):
                            return choices_values[choice-1]
                        else:
                            continue
                except ValueError:
                    print('Invalid response, try again...')
        elif isinstance(prompts_and_choices, list):
            choices_list = list(prompts_and_choices)
            counter = 1
            for i,item in enumerate(prompts_and_choices):
                print(f'{i+1} : {item}')
                counter = i+1
            print('-------------------')
            while True:
                try:
                    choice = int(input(f'Please type a corresponding number for one of the {len(prompts_and_choices)} choices: '))
                    if check_if_num_in_list(choice,choices_list):
                        if y_n_q(f'Is <{choice}> correct?'):
                            return choices_list[choice-1]
                        else:
                            continue
                except ValueError:
                    print('Invalid response, try again...')
    except ValueError:
        exit('Incorrect argument type')


#endregion
#region ARGPARSE

#TODO impliment multicommand as nested library
import multicommand
