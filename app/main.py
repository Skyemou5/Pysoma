#!/usr/bin/python3

#region HEADER

import argparse
import array
import collections
import contextlib
import fnmatch
import functools
import glob
import json
import operator
import os
import pathlib
import pprint

import re
import shutil
from sqlite3 import DataError

import sys

import tkinter as tk
from array import ArrayType
from curses import nonl
from dataclasses import asdict, astuple, dataclass
from functools import lru_cache, reduce
from importlib.resources import path
from itertools import chain, repeat
from pathlib import Path, PurePath
#########################################
#########################################
#########################################
from pprint import pprint
from pydoc import resolve
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
import lib.flatdict as flatdict


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
#region helper funcs
# check OS
def check_os():
    platform = ''
    from sys import platform
    if platform == "linux" or platform == "linux2":
        # linux
        #print("Congrats! You are on linux!")
        platform = "linux"

        pass
    elif platform == "darwin":
        # OS X
        #print("You are on OSX")
        platform = "mac"

        pass
    elif platform == "win32":
        # Windows...
        #print("You are, unfortunately on Windows...")
        platform = "win"

        pass
    else:
        #print("I don't know what system you're on...")
        pass
    return platform

def check_if_num_in_list(num,list) -> bool:
    result = False
    total = len(list)
    if (num > 0) and (num <= len(list)):
        result = True
    else:
        result = False
    return result


def keys_exists(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True


#endregion
#region data classes
# classes
# class NoAliasDumper(yaml.SafeDumper):
#     def ignore_aliases(self, data):
#         return True

# def none_replace(ls):
#     p = None
#     return [p:=e if e is not None else p for e in ls]

# fixing yaml dumping with aliases
class NonAliasingRTRepresenter(ruamel.yaml.representer.RoundTripRepresenter):
    def ignore_aliases(self, data):
        return True



#yaml.representer = NonAliasingRTRepresenter



class ParseYamlLoad(object):
    '''
    Parse yaml from load
    '''
    def __init__(self,data) -> None:
        self.data = data
        self.return_data = self.parse_data(self.data)
        
    # def __repr__(self) -> dict:
    #     return repr(self.return_data)

    def parse_data(self,data) -> dict:
        result = {}
        for document in data:

            for k,v in document.items():
                if isinstance(v,list):
                    self.parse_data(v)
                else:
                    result[k]=v
        # pprint(result)
        jdata = json.dumps(result)
        result = json.loads(jdata)
        # pprint(result)
        return result



class ConfigObject(object):
    def __init__(self) -> None:
        pass
    def convert_paths(self,data):
        temp_obj = data.copy()
        def traverse_data(data):
            for k,v in data.items():
                if isinstance(v,dict):
                    traverse_data(v)
                elif isinstance(v,list):
                    for item in v:
                        traverse_data(item)
                elif isinstance(v,pathlib.Path):
                    data[k]=str(v)
        traverse_data(temp_obj)
        return temp_obj
    def write_dotenv(self,data,path):
        fp = Path(path)
        converted_data = self.convert_paths(data)
        flattened_data = flatten_dict(converted_data)
        with fp.open("w",encoding="utf-8") as f:
            for key, value in flattened_data.items():
                f.write('%s="%s"\n' % (key, value))
    def read_dotenv(self,path):
        from dotenv import dotenv_values
        env_dict = dotenv_values(path)
        import lib.flatdict as flatdict
        result = flatdict.FlatDict(env_dict,delimiter=':')
        return result




class ConfigData(object):
    '''
    Base class for the config object handles general yaml reading and writing
    init argument path to yaml file
    '''
    def __init__(self,config) -> None:
        self.yaml = ruamel.yaml.YAML(typ="rt",pure=True)
        self.config = config
        self.config_file = pathlib.Path(self.config)
        self.data = self.load_file(self.config_file)
        
    def load_file(self,file_path):
        result = {}
        with file_path.open('r') as f:
            try:
                conf = self.yaml.load_all(f)
                cd = ParseYamlLoad(conf).return_data
                return cd
            except yaml.YAMLError as exc:
                print(exc)

        return result
    def update_dict(self,other_dict):
        self.data.update(other_dict)
    def write_file(self):
        #pprint(self.data)
        converted_data = self.convert_paths(self.data)
        #pprint(converted_data)
        # monkey patch:
        ruamel.yaml.representer.RoundTripRepresenter.ignore_aliases = lambda x, y: True
        # pprint(self.data)
        with self.config_file.open('w') as f:
            self.yaml.default_flow_style = False
            self.yaml.dump(dict(converted_data),f)
            # f.write(str(self.yaml.dump(dict(self.data),self.config_file,default_flow_style=False)))
    # def update_and_write_config(self):
    #     self.update_dict()
    #     self.write_config()

    def refresh(self):
        self.data = self.load_file(self.config_file)
    def update(self):
        #print('Updating File....')
        self.write_file()
    def print_data(self):
        print('printing config data...... ')
        pprint(self.data)
    def convert_paths(self,data):
        temp_obj = data.copy()
        def traverse_data(data):
            for k,v in data.items():
                if isinstance(v,dict):
                    traverse_data(v)
                elif isinstance(v,list):
                    for item in v:
                        if isinstance(item,dict):
                            traverse_data(item)
                        elif isinstance(v,pathlib.Path):
                            data[k]=str(v)
                elif isinstance(v,pathlib.Path):
                    data[k]=str(v)
        traverse_data(temp_obj)

        return temp_obj

class ProjectParse(object):
    def __init__(self,config_data) -> None:
        self.yaml = YAML(typ="safe")
        # self.config = ConfigData(pathlib.Path(data))
        self.project_config_data = config_data
        self.config_dir = pathlib.Path(self.project_config_data['config']).parents[0]
        self.project_data_file = pathlib.Path(self.config_dir)/'project_data.yml'
        self.project_data_config = ConfigData(self.project_data_file)
        self.project_data = ProjectData()
        self.project_data.update_from_dict(self.project_data_config.data)
        self.project_data_template_file = pathlib.Path(self.config_dir)/'project_template.yml'
        self.project_template_config = ConfigData(self.project_data_template_file)
        self.enviornment_variables = {}

    def refresh_project_data(self):
        env_vars = {}
        hou_vars = {}
        new_template = dict(self.project_template_config.data['None'])
        def process_dirs(data,path):
            nonlocal env_vars
            nonlocal hou_vars
            current_path = pathlib.Path(path).joinpath(data['name'])
            data['path']=current_path
            # create_dir_if_not_present(current_path)
            if data['env'] is not None:
                env_vars[data['env']]=current_path
            if data['h_env'] is not None:
                if data['h_env'] in hou_vars:
                    #print('item exists')
                    print(hou_vars[data['h_env']])
                    #print(f'{data["h_env"]} + {hou_vars[data["h_env"]]}')
                else:
                    hou_vars[data['h_env']]=current_path
            if data['name']=='.config':
                self.config_path = pathlib.Path(current_path)

            if data['children'] is not None:
                for obj in data['children']:
                    # pprint(obj)
                    process_dirs(obj,current_path)
        print(self.project_config_data['path'])
        #self.new_template['name']=config_data['name']
        process_dirs(new_template,self.project_config_data['path'])
        self.enviornment_variables['env_vars']=env_vars
        self.enviornment_variables['houdini_vars']=hou_vars
        #self.project_template_config.data = new_template
        self.project_template_config.update_dict(new_template)
        self.update_configs()
    def convert_paths(self,data):
        temp_obj = data.copy()
        def traverse_data(data):
            for k,v in data.items():
                if isinstance(v,dict):
                    traverse_data(v)
                elif isinstance(v,list):
                    for item in v:
                        traverse_data(item)
                elif isinstance(v,pathlib.Path):
                    data[k]=str(v)
        traverse_data(temp_obj)

        return temp_obj

    def write_file(self,data,path):
        converted_data = self.convert_paths(data)
        # pprint(converted_data)
        # monkey patch:
        ruamel.yaml.representer.RoundTripRepresenter.ignore_aliases = lambda x, y: True
        # pprint(self.data)
        fp = pathlib.Path(path)
        with fp.open('w') as f:
            self.yaml.default_flow_style = False
            self.yaml.dump(dict(converted_data),f)

    def update_configs(self):
        self.project_template_config.write_file()
        self.project_data.update_paths(self.project_config_data)
        self.project_data.env = self.enviornment_variables
        #pprint(vars(self.project_data))
        self.write_file(dict(vars(self.project_data)),self.project_config_data['config'])

class ProjectSetup(object):

    def __init__(self,template_path=None) -> None:
        #self.keys_path = keys_path
        # self.data = data
        # project_template.yml
        self.yaml = YAML(typ="safe")
        self.template_path = template_path
        self.project_temp_file = self.set_template_path(self.template_path)
        self.config = ConfigData(self.project_temp_file)
        self.data = self.config.data
        self.project_data = self.data['None']['project_root']
        self.shot_data = ShotData()
        self.shot_template = self.shot_data.data
        self.enviornment_variables = {}
        self.config_path = None
        self.new_template = None
    def set_template_path(self,path):
        '''
        Sets application default if none is provided
        '''
        if self.template_path is None:
            return pathlib.Path(application_path)/'project_template_master.yml'
        else:
            return path
    def create_configs(self,c_data):
        #print(c_data['config'])
        #print(self.config_path)
        converted_data = self.config.convert_paths(c_data)
        # monkey patch:
        ruamel.yaml.representer.RoundTripRepresenter.ignore_aliases = lambda x, y: True
        # pprint(self.data)
        fp = pathlib.Path(self.config_path)/'project_data.yml'
        with fp.open('w') as f:
            self.yaml.default_flow_style = False
            self.yaml.dump(dict(converted_data),f)
            # f.write(str(self.yaml.dump(dict(self.data),self.config_file,default_flow_style=False)))
        # self.save_templates()
    def save_templates(self):
        template_list = [
            {
                'data':self.new_template,
                'filename':'project_template.yml'
            },
            {
                'data':self.shot_template,
                'filename':'shot_template.yml'
            }
            ]
        for item in template_list:
            #print('data')
            #print(type(item['data']))
            data = {}
            if isinstance(item['data'],list):
                print(type(item['data'][0]))
                print(item['data'][0])
                data['None'] = item['data']
            if isinstance(item['data'],dict):
                data['None']=item['data']
            converted_data = self.config.convert_paths(data)
            ruamel.yaml.representer.RoundTripRepresenter.ignore_aliases = lambda x, y: True
            fp = pathlib.Path(self.config_path)/item['filename']
            with fp.open('w') as f:
                self.yaml.default_flow_style = False
                self.yaml.dump(dict(converted_data),f)

    def create_project(self,config_data):
        #pprint(self.shot_data.data)
        env_vars = {}
        hou_vars = {}
        #self.new_template = config_data
        new_tempalte = config_data
        def create_dir_if_not_present(dirpath):
            if not dirpath.exists():
                #print(f'+D/..........................Creating new {dirpath.name} Directory in {dirpath.parent}...')
                pathlib.Path(dirpath).mkdir(parents=True,exist_ok=True)
            else:
                #print(f'!!!--------------Directory <{dirpath.name}> in {dirpath.parent} exists! Skipping...')
                pass
        def add_gitkeep(path):
            fp = pathlib.Path(path)/'.gitkeep'
            fp.open("w",encoding="utf-8")
        def add_file(path,f):
            fp = pathlib.Path(path)/f
            fp.open("w",encoding="utf-8")

        test_root = pathlib.Path(application_path)

        def process_dirs(data,path):
            nonlocal env_vars
            nonlocal hou_vars
            current_path = pathlib.Path(path).joinpath(data['name'])
            data['path']=current_path
            create_dir_if_not_present(current_path)

            if data['gitkeep']:
                add_gitkeep(current_path)
            if data['files'] is not None:
                add_file(current_path,data['files'])
            if data['env'] is not None:
                env_vars[data['env']]=current_path
            if data['h_env'] is not None:
                if data['h_env'] in hou_vars:
                    print('item exists')
                    print(hou_vars[data['h_env']])
                    #print(f'{data["h_env"]} + {hou_vars[data["h_env"]]}')
                else:
                    hou_vars[data['h_env']]=current_path
            if data['name']=='.config':
                self.config_path = pathlib.Path(current_path)
            # if config is not None and data['name']=='.config':
            #     create_project_config(current_path,config)
            if data['children'] is not None:
                for obj in data['children']:
                    # pprint(obj)
                    process_dirs(obj,current_path)

        if config_data is not None:
            self.project_data['name']=config_data['name']
            process_dirs(self.project_data,config_data['parent_path'])
        else:
            process_dirs(self.project_data,test_root)

        self.new_template = self.project_data

        self.enviornment_variables['env_vars']=env_vars
        self.enviornment_variables['houdini_vars']=hou_vars

class DotenvData(ConfigObject):
    def __init__(self,data,file_path) -> None:
        self.data = data
        self.file_path = file_path
    def read_data(self):
        self.data = self.read_dotenv(self.file_path)
    def write_data(self):
        self.write_dotenv(self.data,self.file_path)


@yaml_object(yaml)
class ShotConfig(object):
    yaml_tag = u'!project'
    def __init__(self) -> None:
        self.initialized = None
        self.name = None
        self.index = None
        self.users = None
        self.init_date = None
        self.project_root = None
        self.parent_path = None
        self.env = None
        self.path = None
        self.config = None
        self.project_config = None
        self.env_file = None
        self.description = None
    def main_config_list_data(self):
        result = {}
        result['name']=self.name
        result['path']=self.path
        result['config']=pathlib.Path(self.config)/'shot_data.yml'
        return result
    def has_attr(self,attr:str):
        return hasattr(self, attr)
    def update_paths(self,config_data):
        self.path = config_data['path']
        self.parent_path = pathlib.Path(config_data['path']).parents[0]
        self.config = config_data['config']
        self.project_root = config_data['path']
        self.shots = config_data['shots']
    def load_from_file(self,path):
        yaml = YAML()
        new_path = None
        if isinstance(path,str):
            new_path = pathlib.Path(path)
        else:
            new_path = path
        result = {}
        with new_path.open('r') as f:
            try:
                conf = yaml.load_all(f)
                result = ParseYamlLoad(conf).return_data

            except yaml.YAMLError as exc:
                print(exc)
        self.update_from_dict(result)
    def update_from_dict(self, my_dict):
        #print('updating obj')
        #pprint(my_dict)
        for key, value in my_dict.items():
            if self.has_attr(key):
                for a in dir(self):
                    if not a.startswith('__') and not callable(a) and a == key:
                        setattr(self,a,value)
                        #print(getattr(self,a))
    @classmethod
    def to_yaml(cls,representer,node):
        return representer.represent_scalar(cls.yaml_tag,u'{.initialized}-{.name}-{.users}-{.init_date}'.format(node,node))
    @classmethod
    def from_yaml(cls,constructor,node):
        return cls(*node.value.split('-'))

class ShotData(ConfigObject):
    '''
    Initialize with project data or no data
    '''
    def __init__(self,project_data: ConfigData=None) -> None:
        self.yaml = ruamel.yaml.YAML()
        self.project_data = project_data
        #self.choose_temp_file(project_data)
        if project_data is None:
            self.project_temp_file = pathlib.Path(application_path)/'project_template_master.yml'
            self.config = ConfigData(self.project_temp_file)
            self.data = self.config.data['None']['shot_subdir_data']
            self.shots_dir = None
            self.shots_list = None
        else:
            self.project_temp_file = pathlib.Path(self.project_data.data['None']['config'])/'shot_template.yml'
            self.config = ConfigData(self.project_temp_file)
            self.data = self.config.data['None']
            self.shots_dir = self.project_data.data['None']['shots']
            self.shots_list = None
            self.shot_dir_list()
        self.last_opened = None
        self.enviornment_variables = {}
        self.shot_config = ShotConfig()
        self.env_data = None
    def open_shot(self,choice):
        pass
    def update_last_opened(self,choice):
        pass
    def write_file(self,data,file_path):
        # pprint(data)
        converted_data = self.convert_paths(data)
        #pprint(converted_data)
        # monkey patch:
        ruamel.yaml.representer.RoundTripRepresenter.ignore_aliases = lambda x, y: True
        # pprint(self.data)
        with file_path.open('w') as f:
            self.yaml.default_flow_style = False
            self.yaml.dump(dict(converted_data),f)
    def read_file(self,file_path):
        result = {}
        with file_path.open('r') as f:
            try:
                conf = self.yaml.load_all(f)
                cd = ParseYamlLoad(conf).return_data
                return cd
            except yaml.YAMLError as exc:
                print(exc)
        return result

    def shot_dir_list(self):
        '''
        Scans Shot directory and returns a sorted list of shots
        '''
        shots_only=[]
        sorted_shots=[]
        sorted_shot_names=[]
        shot_name_list=[]
        #print(self.data['shots'])
        if any(Path(self.shots_dir).iterdir()):
            for p in Path(self.shots_dir).iterdir():
                if p.is_dir():
                    shot_name_list.append(p.name)
            shots_only = [x for x in shot_name_list if re.match(r"^shot_\d+$", x)]
            sorted_shot_names = sorted(shots_only,key=lambda x: x.split('_')[1])
            #print(f'sorted shots::: {sorted_shot_names}')
            for p in sorted_shot_names:
                np = pathlib.Path(self.shots_dir)/p
                sorted_shots.append(np)
        #print(sorted_shots)
        self.shots_list = sorted_shots
    def create_shot_config(self):
        self.shot_dir_list()
        self.shot_config.env = self.enviornment_variables
        self.shot_config.project_root = self.project_data.data['None']['path']
        self.shot_config.config = pathlib.Path(self.shot_config.path)/'.config/shot_data.yml'
        self.shot_config.env_file = pathlib.Path(self.shot_config.path)/'.config/shot.env'
        self.shot_config.initialized = True
        self.shot_config.project_config = self.project_data.config
        config_data = {}
        config_data['None']=vars(self.shot_config)
        self.write_file(config_data,self.shot_config.config)
        string_shots_list = []
        for item in self.shots_list:
            string_shots_list.append(str(item))
        self.project_data.data['None']['shot_list']=string_shots_list
        self.project_data.write_file()
        #pprint(vars(self.shot_config))
    def create_env_file(self):
        pass
    def create_shot(self,amount=None):
        '''
        Check if first shot folder exists, if not, create it. If folders exists count them and create a new one incremented
        '''
        self.shot_config = ShotConfig()
        #ensure top-level 'shots' exists
        #top_level_shot = Path(Path(Path.cwd().parent)) / "Main_Project/shots"
        #TODO fix this
        top_level_shot = pathlib.Path(self.shots_dir)
        self.shot_config.parent_path = top_level_shot

        # if not Path.is_dir(top_level_shot):
        #     Path.mkdir(top_level_shot)
        
        # print(top_level_shot)
        #case 1 - creating first shot directory
        first_shot_n = Path(top_level_shot)/'shot_1'
        #print(first_shot_n)
        #print(first_shot_n.is_dir())
        if not first_shot_n.is_dir():
            # Path.mkdir(first_shot_n)
            # shot_subfolders = self.create_shot_subfolders(first_shot_n)
            # print(f'{first_shot_n.name} created...')
            # #shot_env_var_init(first_shot_n,shot_subfolders)
            self.shot_config.path = first_shot_n
            self.create_shot_subfolders(first_shot_n)
            self.shot_config.index = 1
            self.shot_config.name = first_shot_n.name
            print(f"\'{first_shot_n}\' created along with resource dirs.")
            self.create_shot_config()
        #case 2 - creating any subsequent shot directory
        else:
            shot_n = first_shot_n
            #skip existing shot directories...
            while Path.is_dir(shot_n):

                shot_name = shot_n.name
                #incremented_number = int(shot_n.name.parts[1].split('_')[1])+1
                incremented_number = int(shot_name.split('_')[1])+1
                self.shot_config.index = incremented_number
                updated_shot_n = shot_name.replace(shot_name.split('_')[1],str(incremented_number))
                shot_n = Path(top_level_shot)/updated_shot_n
                
            #make the new shot directory...

            #create resources for the new shot directory

            self.shot_config.path = shot_n
            self.shot_config.name = shot_n.name
            self.create_shot_subfolders(shot_n)
            print(f"\'{shot_n}\' created along with resource dirs.")
            self.create_shot_config()


    def create_shot_subfolders(self,shot_n):
        #pprint(self.shot_data.data)
        env_vars = {}
        hou_vars = {}
        
        #pprint(self.data)
        #self.new_template = config_data
        new_template = dict(self.data)
        new_shot_path = pathlib.Path(self.shots_dir)/shot_n
        def create_dir_if_not_present(dirpath):
            if not dirpath.exists():
                #print(f'+D/..........................Creating new {dirpath.name} Directory in {dirpath.parent}...')
                pathlib.Path(dirpath).mkdir(parents=True,exist_ok=True)
            else:
                #print(f'!!!--------------Directory <{dirpath.name}> in {dirpath.parent} exists! Skipping...')
                pass
        def add_gitkeep(path):
            fp = pathlib.Path(path)/'.gitkeep'
            fp.open("w",encoding="utf-8")
        def add_file(path,f):
            fp = pathlib.Path(path)/f
            fp.open("w",encoding="utf-8")

        def process_dirs(data: dict,path: pathlib):
            nonlocal env_vars
            nonlocal hou_vars
            current_path = pathlib.Path(path).joinpath(data['name'])
            data['path']=current_path
            create_dir_if_not_present(current_path)

            if data['gitkeep']:
                add_gitkeep(current_path)
            if data['files'] is not None:
                add_file(current_path,data['files'])
            if data['env'] is not None:
                env_vars[data['env']]=current_path
            if data['h_env'] is not None:
                if data['h_env'] in hou_vars:
                    print('item exists')
                    print(hou_vars[data['h_env']])
                    #print(f'{data["h_env"]} + {hou_vars[data["h_env"]]}')
                else:
                    hou_vars[data['h_env']]=current_path
            if data['name']=='.config':
                self.config_path = pathlib.Path(current_path)
            # if config is not None and data['name']=='.config':
            #     create_project_config(current_path,config)
            if data['children'] is not None:
                for obj in data['children']:
                    # pprint(obj)
                    process_dirs(obj,current_path)
        #print(new_template['name'])
        new_template['name']=shot_n.name
        print(f"folder name: {new_template['name']}")

        process_dirs(new_template,self.shots_dir)
        #pprint(new_template)
        #pprint(f'{new_template=}')


        #self.project_data.update_dict(new_template)
        self.enviornment_variables['env_vars']=env_vars
        self.enviornment_variables['houdini_vars']=hou_vars

class HouData(ConfigData):
    def __init__(self,shot_data: ShotData) -> None:
        self.shot_data = shot_data
        self.data = None
        self.gather_env_vars()
    def gather_env_vars(self):
        shot_config = self.shot_data.shot_config
        project_config = self.shot_data.config
        project_data = ProjectData()
        # project_data_config = ConfigData(pathlib.Path(self.shot_data.data['None']['project_config']))
        # project_data.update_from_dict(project_data_config.data)
        # project_vars = project_data_config.env
        # pprint(project_vars)
        shot_vars = shot_config.env
        pprint(project_config.data)

        pprint(shot_vars)
    def prepare_env_vars(self,data):
        pass

class MainConfig(object):
    def __init__(self) -> None:
        self.config_path = pathlib.Path(pathlib.Path(application_path)/'main_config.yml')
        self.config = ConfigData(self.config_path)
        self.data = self.config.data
        self.project_list = self.parse_projects()
        self.load_last = self.data['None']['appdata']['open_last']
        self.last_opened = self.data['None']['appdata']['last_opened']
    def parse_projects(self):
        result = []
        if self.data['None']['projects'] is not None:
            for item in self.data['None']['projects']:
                result.append(item)
        return result
    def refresh_projects(self):
        self.project_list = self.parse_projects()
    def update_projects(self):
        self.data['None']['projects']=self.project_list
    def update_last_opened(self,data):
        self.last_opened = data
        self.data['None']['appdata']['last_opened'] = self.last_opened
        self.config.update_dict(self.data)
    def add_project(self,data):
        if data not in self.project_list:
            self.project_list.append(data)
            self.data['None']['projects']=self.project_list
        
        #self.update_config()
    def remove_project(self,data):
        pass
    def update_config(self):
        self.config.update_dict(self.data)
    def write_config(self):
        self.config.update()
    def update_and_write_config(self):
        self.update_config()
        self.write_config()
    def get_hou_path(self,data):
        result = ''
        houdini_versions = self.data['None']['houdini_versions']
        for majv in houdini_versions:
            for k in majv.keys():
                try:
                    if k == data.houdini_major_version:
                        for minv in majv[data.houdini_major_version]:
                            for kk,v in minv.items():
                                try:
                                    if kk == data.houdini_minor_version:
                                        result = pathlib.Path(v[check_os()])
                                    else:
                                        raise ValueError
                                except ValueError:
                                    exit('config likely has incorrect houdini versions')
                    else:
                        raise ValueError
                except ValueError:
                    exit('config likely has incorrect houdini versions')
        return result


@yaml_object(yaml)
class UserData(object):
    def __init__(self) -> None:
        self.name = None
        self.houdini_license = None
        self.operating_system = None
    @classmethod
    def to_yaml(cls,representer,node):
        return representer.represent_scalar(cls.yaml_tag,u'{.initialized}-{.name}-{.users}-{.init_date}'.format(node,node))

    @classmethod
    def from_yaml(cls,constructor,node):
        return cls(*node.value.split('-'))


@yaml_object(yaml)
class ProjectData:
    yaml_tag = u'!project'
    def __init__(self) -> None:
        self.initialized = None
        self.name = None
        self.users = None
        self.init_date = None
        self.houdini_major_version = None
        self.houdini_minor_version = None
        self.houdini_install_path = None
        self.name = None
        self.project_root = None
        self.parent_path = None
        self.env = None
        self.path = None
        self.config = None
        self.shots = None
        self.shot_list = None
        self.open_last_shot = None
        self.last_opened_shot = None
    def main_config_list_data(self):
        result = {}
        result['name']=self.name
        result['path']=self.path
        result['config']=pathlib.Path(self.config)/'project_data.yml'
        return result
    def has_attr(self,attr:str):
        return hasattr(self, attr)
    def update_paths(self,config_data):
        self.path = config_data['path']
        self.parent_path = pathlib.Path(config_data['path']).parents[0]
        self.config = config_data['config']
        self.project_root = config_data['path']
        self.shots = config_data['shots']
    def load_from_file(self,path):
        yaml = YAML()
        new_path = None
        if isinstance(path,str):
            new_path = pathlib.Path(path)
        else:
            new_path = path
        result = {}
        with new_path.open('r') as f:
            try:
                conf = yaml.load_all(f)
                result = ParseYamlLoad(conf).return_data

            except yaml.YAMLError as exc:
                print(exc)
        self.update_from_dict(result)

    def update_from_dict(self, my_dict):
        #print('updating obj')
        #pprint(my_dict)
        for key, value in my_dict['None'].items():
            if self.has_attr(key):
                for a in dir(self):
                    if not a.startswith('__') and not callable(a) and a == key:
                        setattr(self,a,value)
                        #print(getattr(self,a))


    @classmethod
    def to_yaml(cls,representer,node):
        return representer.represent_scalar(cls.yaml_tag,u'{.initialized}-{.name}-{.users}-{.init_date}'.format(node,node))

    @classmethod
    def from_yaml(cls,constructor,node):
        return cls(*node.value.split('-'))

class Dict2Class(object):
    def __init__(self,my_dict) -> None:
        for k in my_dict:
            setattr(self,k,my_dict[k])


# pdata = ProjectData()
# pdata.houdini_major_version = '18.5'
# pdata.houdini_minor_version = '759'

# mc = MainConfig()
# pdata.houdini_install_path = mc.get_hou_path(pdata)
# mc.add_project(vars(pdata))
# mc.config.convert_paths()


# # class testing
# project_data = ProjectSetup()
# main_config = MainConfig()

# new_project_data = ProjectListData()
# new_project_data.name = 'test_project_2'

# main_config.add_project(vars(new_project_data))
# main_config.update_config()
# main_config.config.update()
# # pprint(main_config.data)
# #project_data.

# new_shot = ShotData()
# # for obj in new_shot.data:
# #     print(obj['name'])

#endregion
#region HELPER METHODS
#region Directory Setup helper methods

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
#region Directory Definitions

###########################################
########### folder dir lists ##############
###########################################

#region global dir names

###################################################
############# Global resource dirs ################
###################################################


#endregion
#region init folder helper functions

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
#region Hou shot env setup
# def shot_env_var_init(shot_path,shot_dirlist):
#     # add_readme_file_to_dir(shot_root)
#     # shot_resource_list = get_resource_paths(shot_root)
#     # for i in shot_dirlist:
#     #     shot_env_dict[i.name]=i
#     # pprint(shot_env_dict)
#     add_dirlist_to_dict(shot_dirlist,'')
#     #shot_dict = add_dirlist_to_return_dict(shot_resource_list)
#     #print(f'Shot dict:::: {shot_dict}')
#     # configure hou vars from existing paths
#     # packages
#     # HDAs
#     # vars HSITE, HOUDINI_PACKAGE_DIR, JOB, HIP, HOUDINI_OTL_SCAN_PATH, HOUDINI_NO_ENV_FILE
#     #print(shot_path)
#     add_var_to_dict('SHOT_NAME',shot_path.name)
#     #add_var_to_dict('HOUDINI_NO_ENV_FILE',True)
#     add_var_to_dict('HSITE',env_dict['HSITE'])
#     add_var_to_dict('HOUDINI_PACKAGE_DIR',env_dict['PACKAGES'])
#     add_var_to_dict('JOB',shot_path)
#     #hda_paths = env_dict['G_HDA']+':'+env_dict['HDA']
#     hda_paths = str(f'{env_dict["G_HDA"]};{env_dict["HDA"]}')
#     add_var_to_dict('HOUDINI_OTLSCAN_PATH',hda_paths)
#     add_var_to_dict('HOUDINI_SCRIPT_PATH',env_dict['SCRIPTS'])
#     add_var_to_dict('HOUDINI_TEXTURE_PATH',env_dict['TEXTURE'])
#     add_var_to_dict('HOUDINI_GEOMETRY_PATH',env_dict['GEO'])
#     add_var_to_dict('HOUDINI_CLIP_PATH',env_dict['CLIPS'])
#     add_var_to_dict('HOUDINI_VEX_PATH',env_dict['VEX'])
#     #print(hda_paths)
#     #add_var_to_dict('HIP',shot_env_dict['HIP'])

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

#endregion

#region Choose Project Dir
# Project stuff
# def choose_proj_dir():
#     global env_dict
#     proj_name = env_dict['PROJECT_NAME']
#     print(proj_name)
#     #global PROJECT_ROOT
#     if(y_n_q('Do you want to use the current directory?')):
#         #PROJECT_ROOT = pathlib.Path(__file__)
#         new_path = pathlib.Path(application_path)/proj_name
#         PROJECT_ROOT = new_path
#         add_var_to_dict('PROJECT_ROOT',new_path)

#     else:
#         while True:
#             try:
#                 user_input = input('Please type in desired path: ').lower()
#                 input('Please note the name you chose will be appended to end of the path you set...')
#                 new_path = pathlib.Path(user_input)/proj_name
#                 print(new_path.is_dir())
#                 if new_path.is_dir():
#                     if(y_n_q(f'Is {str(new_path)} the correct path?')):
#                         add_var_to_dict('PROJECT_ROOT',new_path)
#                         print(env_dict['PROJECT_ROOT'])
#                         #PROJECT_ROOT = new_path
#                         break
#                     else:
#                         continue
#                 else:
#                     raise FileNotFoundError
#             except FileNotFoundError:
#                 print('Directory is not valid! Please try again...')
#                 continue
#     print(f'You have chosen {PROJECT_ROOT} as your main project directory')
#     input('Press Enter to continue...')


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
                    choice = int(input(f'Please type a corresponding number for one of the {len(prompts_and_choices)} choices: '))
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
main_config = MainConfig()
# TODO:convert to yaml from config
def projects_init_main() -> tuple:
    # args

    def create_project(name=None,root_path=None) -> ConfigData:

        print('Creating a new project...')
        main_config.data['None']['appdata']['initialized']=True
        if name is None:
            project_name = set_project_name()
        else:
            project_name = name
        
        project_data = ProjectData()
        project_data.name = project_name

        if root_path is None:
            choice = user_choose_folder_methods_noscan()
            path = choose_folder_method(choice)
        else:
            path = root_path
        
        project_data.parent_path = pathlib.Path(path)

        project_path = pathlib.Path(path)/project_data.name

        project_data.path = project_path
        
        new_project = ProjectSetup()
        new_project.create_project(vars(project_data))
        project_data.config = new_project.config_path
        
        project_data.env = new_project.enviornment_variables
        # not fully initialized until shot decision
        project_data.initialized = False
        project_data.project_root = project_path
        project_data.name = project_name
        # set houdini version

        project_data.houdini_major_version = '18.5'
        project_data.houdini_minor_version = '759'
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
            new_project_config = ConfigData(project_data.config)

            return new_project_config
        # pprint(vars(project_data))

    def add_existing_project(project_path=None) -> tuple:

        while True:
            
            if project_path is None:
                project_path = choose_folder_method(user_choose_folder_methods_noscan())
                
            config_path = pathlib.Path(project_path)/'.config/project_data.yml'
            for project in main_config.project_list:
                if project['path'] == str(project_path):
                    print(f'Project <{project["name"]}> already exists!')
                    print('pick another folder or exit...')
                    continue
            try:
                if config_path.exists():
                    project_data = ProjectData()
                    return ConfigData(config_path), project_data.update_from_dict(ConfigData(config_path).data['config'])

                
            except:
                print('not a valid project please choose another folder')
                continue
        #return new_project_config

    def choose_existing_project() -> tuple:

        print('The following projects exist...')
        for i, item in enumerate(main_config.project_list):
            print(f'{i+1} : {item["name"]}')
        choice = choose_project_from_list(main_config.project_list)
        #print(choice)
        chosen_project = main_config.project_list[choice[0]-1]
        #chosen_project['last_opened']=True
        main_config.update_projects()
        main_config.update_config()
        main_config.write_config()
        #print(chosen_project['config'])
        # project_data = ConfigData(pathlib.Path(chosen_project['config'])/'project_data.yml')
        project_data = ProjectData()
        new_project_config = ConfigData(chosen_project['config'])
        #pprint(new_project_config.data)
        #project_data.from_yaml(new_project_config.data)
        project_data.load_from_file(chosen_project['config'])
        #pprint(vars(project_data))

        return new_project_config, project_data
        # pprint(main_config.data)
        # pprint(project_data.data)

    def open_project(project_data: ProjectData) -> tuple:
        #pprint(project_data.data)
        #pprint(main_config.data)
        print(f'Opening project <{project_data.data["None"]["name"]}> .......')
        project_data_obj = ProjectData()
        project_data_obj.update_from_dict(project_data.data)
        main_config.update_last_opened(project_data_obj.main_config_list_data())
        main_config.update_and_write_config()
        #pprint(vars(project_data_obj))
        return project_data

    def user_choice_list(choice_dict:dict) -> ConfigData:
        while True:
            project_choice_action = user_choice_from_list(choice_dict)
            project_choice_data = project_choice_action()
            #pprint(project_choice_data.data)
            if y_n_q(f'Do you want to open <{project_choice_data.data["name"]}>'):
                break
            else:
                continue
        return project_choice_data

    def get_last_opened():

        last_opened_data = main_config.data['None']['appdata']['last_opened']
        project_config_data = ConfigData(last_opened_data['config'])
        project_data = ProjectData()
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
                if y_n_q('Do you want to always open the last opened project by default?'):
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
                                if y_n_q('Do you wish to add it?'):
                                    existing_project_config = ConfigData(config_path)
                                    existing_project_data = ProjectData()
                                    existing_project_data.update_from_dict(existing_project_config.data)
                                    main_config.add_project(existing_project_data.main_config_list_data())
                                    main_config.update_and_write_config()
                        else:
                            if y_n_q('Do you want to create project in folder anyway?'):
                                create_project(p.name,root_path.absolute())
                exit()
            elif args.gui_project:
                project_name = set_project_name()
                path = choose_dir_gui()
                create_project(project_name,path)
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
                        create_project(p.name,root_path.absolute())
                    else:
                        print(f'{p.name} is already a directory!')
                        # TODO impliment check for valid projects
                        config_path = pathlib.Path(p)/'.config/project_data.yml'
                        if config_path.is_file():
                            print('and a Valid Project')
                            if item not in project_name_list:
                                print('project not in config')
                                if y_n_q('Do you wish to add it?'):
                                    existing_project_config = ConfigData(config_path)
                                    existing_project_data = ProjectData()
                                    existing_project_data.update_from_dict(existing_project_config.data)
                                    main_config.add_project(existing_project_data.main_config_list_data())
                                    main_config.update_and_write_config()
                        else:
                            if y_n_q('Do you want to create project in folder anyway?'):
                                create_project(p.name,root_path.absolute())


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
                    
                    add_existing_project(p)
                    # /home/ben/dev/Aces_Stuff/Pysoma/app/tt /home/ben/dev/Aces_Stuff/Pysoma/app/ff

                exit()
            elif args.gui_project:
                print('gui')
                pp = choose_dir_gui()
                add_existing_project(pp)
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
                        project_config_data = ConfigData(project['config'])

                if exists:
                    chosen_project=open_project(project_config_data)
                else:
                    print('Project name not recognized...')
                    exit()

            elif args.load_last:
                if main_config.data['None']['appdata']['last_opened'] is not None:
                    project_config_data = ConfigData(main_config.data['None']['appdata']['last_opened']['config'])
                    chosen_project=open_project(project_config_data)
                else:
                    print('No project loaded last...')
                    exit()

            elif args.open_project_list:
                choice = choose_existing_project()
                chosen_project=open_project(choice)

            else:
                exit('please check help and use a correct flag')
        elif args.command == 'shots':
            # pass data to shots
            if main_config.data['None']['appdata']['last_opened'] is not None:
                project_config_data = ConfigData(main_config.data['None']['appdata']['last_opened']['config'])
                chosen_project=open_project(project_config_data)
            else:
                choice = choose_existing_project()
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
            if y_n_q('Do you want to always open the last opened project by default?'):
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
                chosen_project=open_project(get_last_opened())
        else:
            if main_config.config.data['None']['projects'] is None:
                print('There are no projects saved')
                chosen_project = open_project(user_choice_list(initial_project_choices))
            else:
                print('There are projects saved in your config')
                chosen_project = open_project(user_choice_list(project_choices))
        return chosen_project



#endregion
#endregion
#endregion
#endregion
#region Shot Main
#region SHOTS
#region shot subdir definition

###########################################
##############               ##############
############     Shot Prep     ############
##############               ##############
###########################################
#endregion
#region Create Shot
####
shots_list = []
shot_env_dict = {}


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


#endregion


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
    
    #add_dirlist_to_dict(reslist,'')
    
    for i in reslist:

        sublist = []
        print(i.name)
        for k in i.iterdir():
            if k.is_dir():
                print(f'...........{k.name}')
                sublist.append(k)

    # shot_env_dict(path,subdir_list)
    #shot_env_var_init(path,reslist)
#region SHOT MAIN
def shot_main(project_data):
    # helper funcs
    print(project_data)
    def open_shot(shot_actions):
        print('open_shot')
        action = shot_actions
        shot_data = action()
        houdini_data = HouData(shot_data)
        #pprint(vars(shot_data.shot_config))


    def choose_shot() -> ShotData:
        print('choose shot')
        shot_name_list = [x for x in project_data.data['None']['shot_list'].name]
        print(shot_name_list)
        #choice = user_choice_from_list(project_data.data['None']['shot_list'])
        pass
    

    def create_new_shot() -> ShotData:
        shot_data = ShotData(project_data)
        while True:
            shot_data.create_shot()
            if y_n_q('Would you like to open newly created shot?'):
                break
            else:
                continue

        return shot_data

    

    opened_shot_data = None
    # ARGS
    if args.command is not None:
        if args.command == 'shots':
            if args.open_shot:
                print(args.open_shot)
            elif args.create_shot:
                print(args.create_shot)
        else:
            pass
    else:
        ###################################################
        #################     NO ARGS    ##################
        ###################################################
        shot_choices = {
            'Would you like to create a new shot?':create_new_shot,
            'Would you like to open an existing shot?':choose_shot,
        }
        #print('no commands')
        #pprint(project_data.data)
        if project_data.data['None']['shot_list'] is not None:
            # create new shot or open existing shot
            print('shots exist')

            shot_decision = open_shot(user_choice_from_list(shot_choices))


        else:
            # create new shot
            print('no shots exist')
            
            # initialize
            if project_data.data['None']['initialized'] is None or project_data.data['None']['initialized'] is False:
                if y_n_q('Do you want to always open the last opened shot by default?'):
                    project_data.data['None']['open_last_shot']=True
                else:
                    main_config.config.data['None']['open_last_shot']=False
                project_data.data['None']['initialized']=True
                project_data.write_file()
                project_data.refresh()
            else:
                if project_data.data['None']['open_last_shot'] is True:
                    # if shot list is null
                    if project_data.data['None']['shot_list'] is None:
                        opened_shot_data = create_new_shot()

                    # choose shot
                    # if shot doesn't exist
                else:
                    # if shot list is null
                    if project_data.data['None']['shot_list'] is None:
                        pass
                    else:
                        pass
                    # create new shot or pick one



#endregion
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
        add_var_to_dict('FILE_TO_O/app/main.pyPEN','')
        input('Press Enter to continue....')




#endregion
#endregion
#endregion

#endregion
#region MAIN



def main():
    opened_project = projects_init_main()
    shot_data = shot_main(opened_project)

if __name__ == "__main__":
    main()


#endregion
#endregion
