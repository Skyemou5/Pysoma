# Pysoma
A crossplatform Houdini project management and pipeline tool for smaller teams, students, and classrooms.

---
![Pyrosome](./pysomaicon.png?raw=true "Pyrosome")

Pyrsomes are actually colonies of small jellyfish creating a whole. I thought that was a fun way to think about group creative projects. In a way this tool helps multiple people be part of a whole, and because it's houdini, life, mathematics and growth are common insterests of houdini artists.

---

# Houdini Pipeline Tool

This was developed for my needs during my senior project using Houdini with a small team. I needed to ensure the project enviornment was the same accross computers and platforms. Additionally I needed a way to run the tool on it's own without needing to configure each computers python enviornment.

# TODO

- Refactor main file into a library to clean up code
- Build standalone app for each platform
- add support for choosing houdini versions - currently 18.5.759 is hardcoded in for my project
- refactor to properly serialize data with yaml and only use env files for enviornments
- Implement unit testing
- Implement project scanning
- refactor print statements for an actual logging system

# Roadmap
- add support for game projects with unity and unreal and possibly godot
- add support for houdini engine and respective game engines
- add hou.py configuration for opening houdini projects
  - new file
  - default node setup
- possible branch project name pyrasoma?
- possibly rewrite in rust
- add support for houdini package management
- refactor data to json
- add data manager to edit json defaults
- use yaml for configuration
- Add database for viewing assets in project and dependencies



---

# How to use the tool

1. Run it as a python script from the cloned repo.
2. Integrate it into you're system on UNIX systems.
3. Use the compiled versions and rus as an executable.


## There are command line arguments
```bash
usage: main.py [-h] [-pn PATH_PROJECT] [-un [GUI_PROJECT]] [-cn [CURRENT_DIR_PROJECT]] [-pl [LIST_PROJECTS]] [-rs [RESCAN_DIRS]]
               [-cp [CLEAR_CACHE]] [-i [INIT]] [-I [INIT_ONLY]] [-l [LOAD_LAST]] [-? [INFO]]

optional arguments:
  -h, --help            show this help message and exit
  -pn PATH_PROJECT, --path-project PATH_PROJECT
                        create new project at input path
  -un [GUI_PROJECT], --gui-project [GUI_PROJECT]
                        create new project at location with gui
  -cn [CURRENT_DIR_PROJECT], --current-dir-project [CURRENT_DIR_PROJECT]
                        create new project at current path
  -pl [LIST_PROJECTS], --list-projects [LIST_PROJECTS]
                        List currently cached projects
  -rs [RESCAN_DIRS], --rescan-folders [RESCAN_DIRS]
                        rescan cached directories
  -cp [CLEAR_CACHE], --clear-project-cache [CLEAR_CACHE]
                        clear project cache
  -i [INIT], --init [INIT]
                        Forces initialization
  -I [INIT_ONLY], --init-only [INIT_ONLY]
                        Forces ONLY the initialization step
  -l [LOAD_LAST], --load-last [LOAD_LAST]
                        Load last opened file
  -? [INFO], --info [INFO]
                        Shows another help file
```

---

# How it works

## Default behavior

1. Checks if there are any projects in the current directory of the script/app
2. If there are none it creates one after asking for a name
3. Asks user to create or open a shot
4. sources houdini, sets enviornment variables, opens houdini

## Things to note

You can customize this behavior, for example you can add directories for the tool to scan for existing projects.

It saves a list of the existing projects in a hidden temp.env file in the same directory as the script or executable.

Each project will have an env file that shouldn't be pushed to a project repo as it will hold that users paths.

---

# Contributing

Make sure and set up a python virtual env - I used venv - using the requirements.txt


---

# Other

I'm no python expert and would love input, and fixes, especially in development workflows, and deployment systems and such. I'm still learning, but I hope this is useful.


---

Hope this helps someone else, If you have questions send me a message.