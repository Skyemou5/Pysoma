#!/usr/bin/python3

import os
import time
import string
import subprocess
import argparse
import fnmatch
import glob
###
from pathlib import Path

#region VARIABLES

##############################
############ VARS ############
##############################

# Other vars
path_list = []
env_dict = {}

# preset paths
HOME = os.getenv("HOME")
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
#print(REPO_ROOT)


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
#region SETUP
##############################
###### SET UP FOR LATER ######
##############################
#region WORK SETUP METHODS

def get_initial_paths():
    pass



#endregion
#region HELPER SETUP METHODS
###############################
####### DIRECTORY PATHS #######
###############################

def get_path(root,target):
    pass

def set_path():
    pass

def compare_path():
    pass

###############################
######## ENV VAR STUFF ########
###############################

def check_if_var_exists():
    pass

def check_value_of_env_var():
    pass

def compare_env_value():
    pass

def unset_env_var():
    pass

def set_env_var():
    pass

#endregion

#region SETUP MAIN


#endregion
#endregion
#region LOGIC

#region HELPER LOGIC METHODS

###########################
####### User Input ########
###########################

def question_pred():
    pass

###################################
####### Dir & Config Stuff ########
###################################

# directory stuff
def create_dir_list():
    pass

def create_dirs():
    pass

def project_list():
    pass

# config stuff
def create_config_dir():
    pass


def terminal_config_file():
    pass

##############################
####### Houdini Stuff ########
##############################

def get_houdini_version():
    pass

def get_houdini_hython_path():
    pass

def get_hip_file_path():
    pass

def set_hip_file_paths():
    pass

def init_houdini():
    pass

def launch_houdini():
    pass


#endregion
#region WORK LOGIC METHODS

###############################
####### User Interface ########
###############################



#endregion
#region LOGIC FINAL

#endregion
#region EXECUTE
def main():
    pass

#endregion

