#!/usr/bin/python3

import os
import time
import string
import subprocess
import argparse
import fnmatch
import glob

HOU_ROOT = os.getenv('HOU_ROOT')
HOME = os.getenv('HOME')
PROJ_ROOT = ''
HIP = ''

## Launch functions ##

# Decide Houdini Version
def setVersion():
    pass


# Set $JOB
def setProject(NAME):
    PROJ_ROOT = os.path.join(HOU_ROOT, NAME)
    HIP = os.path.join(PROJ_ROOT, "HIP")
    return PROJ_ROOT, HIP
    
# Create list of environment variables to declare
def initHoudini(DIRS=None, PROJ_ROOT=None):
    # This variable is necessary on H19.0.455 due to Houdini bug
    compat = "export LD_PRELOAD=/lib/x86_64-linux-gnu/libc_malloc_debug.so.0 ; "
    cmd = []
    cmd.append(compat)
    cmd.append("export JOB=\"%s\" ; " % PROJ_ROOT)
    # Create env vars for project sub-directories
    for dir in DIRS:
        cmd.append("export %s=\"%s/%s\" ; " % (dir,PROJ_ROOT,dir))
    return cmd
    
# Launch terminal environment
def launch(NAME=None, DIRS=None, PROJ_ROOT=None):
    # Create terminal launch command.
    PROJ_ROOT_Q = "\"" + PROJ_ROOT + "\""
    msg1 = 'echo "To open Houdini, run \'houdini\'"'
    env = initHoudini(DIRS, PROJ_ROOT) 
    filepath = "/tmp/bismuth.env"
    file = open(filepath, "w", 0o777)
    for var in env:
        file.write(var)
    file.write(msg1)
    file.close()
    os.chmod(filepath, 0o777)
        
    term = "gnome-terminal --title=%s --window-with-profile=%s --working-directory=%s" % (NAME, "Houdini\ Env", PROJ_ROOT_Q)
    os.system(term)
    
#--------------------------------------------------------------------------------------
## Config functions ##

# Make directory structure
def createDirs(workingDir=None, DIRS=None):
    if workingDir != None:
        if DIRS is not None:
            for dir in DIRS:
                path = os.path.join(workingDir, dir)
                # If path does not exist, make it.
                if not os.path.isdir(path):
                    os.makedirs(path, 0o755)

# Create list of sub-directories to create
def createDirList():
    dirString = "GEO RENDER HIP BLEND"
    dirs = dirString.split()
    return dirs

# Create config directory
def createConfigDir(configDir):
    # If config directory doesn't exist, make one.
	if not os.path.isdir(configDir):
		print("--> Creating config directory %s" % configDir)
		try:
			os.makedirs(configDir)
		except:
			print("ERROR:  Could not make %s" % configDir)
	if not os.path.isdir(configDir):
		print("ERROR:  Cannot find dir %s" % configDir)
		
def terminalConfigFile():
    configDir = os.path.join(HOME, ".config/bismuth")
    configFile = os.path.join(configDir, "bismuth.term")
		
# Create and access project list
def projectList(value=None, action=None):
    configDir = os.path.join(HOME, ".config/bismuth")
    
    configFile = os.path.join(configDir, "bismuth.history")
    createConfigDir(configDir)
    
    lastentry = ""
    config = ""
    
    # Access contents of config file
    if os.path.isfile(configFile):
        file = open(configFile, "r")
        config = file.read()
        file.close()
        lastentry = config.strip().split("\n")[-1]
    
    # Return config
    if action == "lastentry":
        return config.strip()
        
    if os.path.isdir(configDir):
        # Write new project name project list
        if action == "write":
            if lastentry != value:
                line = "%s" % (value)
                file = open(configFile, "a")
                file.write(line)
                file.write("\n")
                file.close
        # Read from project list
        if action == "read" and os.path.isfile(configFile):
            entry = ""
            
            # Keep five entries
            numentries = len(config.strip().split("\n"))
            
            total = []
            if numentries > 5:
                start = numentries - 4
                count = 1
                f = open(configFile, "w")
                for x in config.strip().split("\n"):
                    count = count + 1
					
                    if x.strip() != "" and count > start:
						# don't allow duplicates in list
                        if x not in total:
                            total.append(x)
                            f.write(x)
                            f.write("\n")
                f.close()
			
			# find the last entry
            for x in config.split("\n"):
                if x.strip() != "":
                    entry = x
            return entry
                
#-------------------------------------------------------------------
# User Interface
dirslist = glob.glob("%s/*/" % HOU_ROOT)
dirs = ""
proj = ""

if len(dirslist) > 0:
    #
    previous = ""
    #projectList(action="write")
    msg1 = "~ Select your project:"
    msg2 = "~ Hit 0 to create a new project.\n"
    print("-" * len(msg1))
    print(msg1)
    
    count = 1
    # Sort by last access date
    file_list = []
    for file in dirslist:
        stats = os.stat(file)
        lastModified = time.localtime(stats[8])
        fileDate = lastModified, file
        file_list.append(fileDate)
    file_list.sort()
    sorted = []
    for file in file_list:
        c = str(count).rjust(2)
        p = file[-1].split("/")[-2]
        sorted.append(p)
        print("%s - %s" % (c, p))
        count = count + 1
    
    # List five most recent projects
    lastfive = projectList(action="lastentry")
    
    addtolength = 0
    if lastfive != "":
        print("\n---- Recent Shots ---")
        addtolength = len(lastfive.strip().split("\n"))
        
        for curr in lastfive.strip().split("\n"):
            c = str(count).rjust(2)
            sorted.append(curr)
            print("%s - %s" % (c, curr))
            count = count + 1
    
    previous = projectList(action="read")
    PREVIOUSDIR = ""
    if previous != None:
        PREVIOUSDIR = os.path.join(HOU_ROOT, previous)
    if os.path.isdir(PREVIOUSDIR):
        msg2 = "\n~ Choose a project to work on. \n- Hit 0 to create a new project. \n- Hit Enter for \"%s\"\n" % previous
        
    # Process user selection of project
    selection = input(msg2)
    # If a number is entered, check validity
    if selection.isdigit():
        # Throw error if selection is out of range.
        if int(selection) > len(dirslist) + addtolength:
            print("ERROR: Out of Range")
            exit(0)
        # If user selects 0, create new project.
        if selection == "0":
            proj = input("~ Enter a name for your project:\n")
        # If in range and non-zero, select the corresponding project.
        else:
            proj = sorted[int(selection) - 1]
    if selection == "":
        proj = previous
# If there are no projects in the root dir, prompt to make a new one.
else:
    proj = input("~ Enter a name for your project:\n")
    
# Set project and create directories, if necessary
if proj != "":
    PROJ_ROOT, HIP = setProject(proj)
    if not os.path.isdir(PROJ_ROOT):
        os.makedirs(PROJ_ROOT)
        
    projectList(value=proj, action="write")
    dirs = createDirList()
    createDirs(PROJ_ROOT, dirs)

#------------------------------------------------------
# Launch
launch(proj, dirs, PROJ_ROOT)


