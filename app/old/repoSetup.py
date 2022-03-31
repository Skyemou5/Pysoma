#!/usr/bin/python3

#region IMPORT

import os
import pathlib
import time
import string
import subprocess
import argparse
import fnmatch
import glob
import sys
import subprocess
import json
import csv
#from tkinter.messagebox import QUESTION
#from msilib.schema import Directory
from itertools import chain, repeat
from pathlib import Path
from os.path import exists
from dotenv import load_dotenv
from pkgutil import iter_modules
from contextlib import nullcontext
#endregion

#region SETUP
env_dict = {}




################################
######## SETUP #################
################################



#### REPO SETUP ####
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) ##!!
root_var = os.environ['HOU_TOOL_REPO'] = ROOT_DIR
env_dict['HOU_TOOL_REPO']=ROOT_DIR

#print(root_var)

#print("root dir " + ROOT_DIR)
dir_list = os.listdir(ROOT_DIR)

HDA_DIR = os.path.join(ROOT_DIR,"HDA") ##!!
env_dict['HDA_DIR']=HDA_DIR
#print(HDA_DIR)
hda_list = os.listdir(HDA_DIR)
#print(hda_list)


### Houdini Package Dir ###

houdini_package_dir = os.path.join(ROOT_DIR,"packages")
#print(HOUDINI_PACKAGE_DIR)
HOUDINI_PACKAGE_DIR_var = os.environ['HOUDINI_PACKAGE_DIR'] = houdini_package_dir ##!!
env_dict['HOUDINI_PACKAGE_DIR']=houdini_package_dir

### OTL Scan path ###

otl_scan = ""
exclude_directories = set(['backup'])
for d in os.listdir(HDA_DIR):
    if not d in exclude_directories:
        #print(d)
        path = os.path.join(HDA_DIR,d)
        #print(path)
        otl_scan += str(path+':')
otl_scan = otl_scan[:-1]
#print(otl_scan+'&')
#otl_scan = otl_scan + '&'


otl_scan_var = os.environ['HOUDINI_OTLSCAN_PATH'] = otl_scan ##!!
#print(os.environ['HOUDINI_OTLSCAN_PATH'])
env_dict['HOUDINI_OTLSCAN_PATH']=otl_scan



#### ACES SETUP ####
etc_path = os.path.join(ROOT_DIR,"etc_assets")
ocio_path = os.path.join(etc_path,"OpenColorIO-Configs")
ocio_config_path_dir = os.path.join(ocio_path,"aces_1.0.3")
ocio_config_path = os.path.join(ocio_config_path_dir,"config.ocio") ##!!
#print(ocio_config_path)



blender_ocio_path = os.path.join(etc_path,"Blender-config")
blender_ocio_config = os.path.join(blender_ocio_path,"config.ocio") ##!!
#print(blender_ocio_config)

#endregion

#region MAIN METHODS

########################################
############# MAIN METHODS #############
########################################

#REGION MAIN METHODS

#print( '\n'.join([f'{k}: {v}' for k, v in sorted(os.environ.items())]) ) # list all env vars
def Configure_OCIO(standard):
    if standard:
        ocio_var = os.environ['OCIO']=ocio_config_path
        env_dict['OCIO']=ocio_config_path
        env_dict['OCIO_BLENDER']=blender_ocio_config
    else:
        ocio_var = os.environ['OCIO']=blender_ocio_config
        env_dict['OCIO']=blender_ocio_config


### How to use info ###

def user_question(prompt):
    answers = {"y","n"}
    prompts = chain([prompt], repeat("Please answer with y/n: "))
    replies = map(input, prompts)
    valid_response = next(filter(answers.__contains__, replies))
    print(valid_response)
    return valid_response


def Env_Configure():

    # OCIO
    ocio = answer_pred("Do you want to configure ACES? ")
    if ocio:
        
        if answer_pred("Do you want the blender config? "):
            Configure_OCIO(False)
        else:
            Configure_OCIO(True)
    
    #### Write to file so system scripts can use it ####
    Write_To_File_Controller()

    # System Vars
    if answer_pred("Do you want to configure system vars?"):
        if answer_pred("do you want to unset system vars? "):
            pass
        if answer_pred("Do you want to set system vars? "):
            #configure_system_vars()
            pass

    # PRINT TO FILE
    # if answer_pred("Do you want to print vars to file? "):
    #     Write_To_File_Controller()

### Set Up System Variables
def configure_system_vars(set):
    write = set
    ### SET System ENVIORNMENT ####
    from sys import platform
    if platform == "linux" or platform == "linux2":
        # linux
        print("Congrats! You are on linux!")
        val = subprocess.check_call("chmod +x setenv.sh" , shell=True)
        pass
    elif platform == "darwin":
        # OS X
        print("You are on OSX")
        val = subprocess.check_call("chmod +x setenv.sh" , shell=True)
        pass
    elif platform == "win32":
        # Windows...
        print("You are, unfortunately on Windows...")
        val = subprocess.check_call("./setenv.bat" , shell=True)
        pass
    else:
        print("I don't know what system you're on...")
        pass

#endregion

#region HELPER METHODS

##########################################
########## HELPER METHODS ################
##########################################


def question_predicate(answer):
    #print(valid_response)
    
    if answer == "y":
        value = True
    elif answer == "n":
        value = False
    return value

def answer_pred(prompt):
    answer = user_question(prompt)
    value = question_predicate(answer)
    return value


def Write_To_File_Controller():
    env_path = pathlib.Path("tools.env")
    json_path = pathlib.Path("tools.json")
    line_to_write = ""
    ### Write to Env
    if env_path.exists():
        print("env file exists")
        #Write to existing file
        Write_To_Env_File(env_path)
    else:
        print("does not exist")
        # Create File
        with open('tools.env', 'w') as fp:
            pass
        Write_To_Env_File(env_path)
    #### Write to JSON
    if json_path.exists():
        print("json exists")
        Write_To_Json(json_path)
    else:
        print("creating json file")
        with open("tools.json","w") as fp:
            pass
        Write_To_Json(json_path)

def Write_To_Env_File(file_path):
    print(file_path)
    with open(file_path, 'w') as f:
        for key, value in env_dict.items():
            f.write('%s="%s:&"\n' % (key, value))

def Write_To_Json(file_path):
    # f = open(file_path, "w")
    # d = json.dumps(env_dict, indent=4)
    # json.dump(d,f)
    # f.close()
    with open(file_path,'w') as fp:
        json.dump(env_dict,fp, indent=4,sort_keys=True)

### Convert paths to system ###
def Convert_Path_To_OS():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        # linux
        print("Congrats! You are on linux!")
        
        pass
    elif platform == "darwin":
        # OS X
        print("You are on OSX")
        
        pass
    elif platform == "win32":
        # Windows...
        print("You are, unfortunately on Windows...")
        
        pass
    else:
        print("I don't know what system you're on...")
        pass
#endregion

#region EXECUTE

####################################
############ EXECUTE ###############
####################################

def Main():
    #init()
    Env_Configure()
    #print(env_dict)
    #Write_To_File_Controller()

Main()

#endregion



# PRINT vals and keys of dictionary
# for key, value in env_dict.items():
#     print(key,'=',value)

