#!/usr/bin/python3
#region HEADER
import contextlib
import os
import pathlib
import string
import argparse
import fnmatch
import glob
import sys
import json
import lib.dotenv
import tkinter as tk
import yaml
import re
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
#endregion
#region data classes

class config_data:
    def __init__(self,config) -> None:
        self.config = config

class project_data:
    def __init__(self,name,path) -> None:
        self.name = name
        self.path = path

class projects_data:
    def __init__(self,projects,scan_dirs) -> None:
        self.projects = projects
        self.scan_dirs = scan_dirs

class project_dirs:
    def __init__(self,project_dir_data) -> None:
        self.project_dir_data = project_dir_data


#endregion
