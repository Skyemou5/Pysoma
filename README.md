<div align="center">
  <img src="./pysomaicon.png" width="200" height="200">
</div>



>Pyrsomes are actually colonies of small jellyfish creating a whole. I thought that was a fun way to think about group creative projects. In a way this tool helps multiple people be part of a whole, and because it's houdini, life, mathematics and growth are common insterests of houdini artists.

---

# Pysoma

A crossplatform Houdini project management and pipeline tool for smaller teams, students, and classrooms.

This was developed for my needs during my senior project using Houdini with a small team. I needed to ensure the project enviornment was the same accross computers and platforms. Additionally I needed a way to run the tool on it's own without needing to configure each computers python enviornment.

# TODO

- [ ] Refactor main file into a library to clean up code
- [ ] add support for choosing houdini versions - currently 18.5.759 is hardcoded in for my project
- [ ] refactor to properly serialize data with yaml and only use env files for enviornments
- [ ] Implement unit testing
- [ ] Implement project scanning
- [ ] refactor print statements for an actual logging system
- [ ] impliment CLI tool that lets you specify a YAML file to use a project template
- [ ] create better documentation


# Roadmap
- [ ] make a docker image so users need less setup
- [ ] add support for game projects with unity and unreal and possibly godot
- [ ] add support for houdini engine and respective game engines
- [ ] add hou.py configuration for opening houdini projects
  - [ ] new file
  - [ ] default node setup
- [ ] possible branch project name pyrasoma?
- [ ] possibly rewrite in rust
- [ ] add support for houdini package management
- [x] use yaml for configuration
- [ ] Add database for viewing assets in project and dependencies
- [ ] add tool for setting up project templates
- [ ] add integration with version control
- [ ] tightly integrate USD
- [ ] network support
- [ ] support renderfarm setups
- [ ] tool for documenting project
- [ ] project report generator



---

# How to use the tool

1. Run it as a python script from the cloned repo.
2. Integrate it into you're system on UNIX systems.
3. Use the compiled versions and rus as an executable.


## There are command line arguments




---
# Setup

If you want to use the GUI option to select file paths on linux you need to have the `python3-tk` package installed on your system. You may need something similar on mac as well.

example (fedora: RHEL):

```bash
sudo dnf install python3-tk -y
```

On widows you may need to install python with `tkinter` or use `Anaconda` to manage all the dependencies for that.


## Unix

>! make sure you have at least python 3.12 installed

Steps:

- Clone the repo to your machine.
- In your terminal navigate to the `/app` folder inside this repo. ex: `cd ./app`
- I have provided a shell script to quickly get you up in running! All you have to do is `source` a file called `activate_enviornment.sh` which is inside the `/app` folder.

```bash
source ./activate_enviornment.sh
```

>It's important you `source` is and not execute the script normally with `bash` or dot-syntax. This is because this script will install a python virtual-enviornment then install all the dependencies from the `requirements.txt` then drop into a subshell where that virtual enviornment is sources. Additionally it creates an alias so all you need to do is type `pysoma` and you can run the app!

Now that you have the enviornment setup and the subshell running you can start to use the program.

running `pysoma` by itself will start the program and use the default entry point.

As this is the first time running the application there won't be any projects saved in the `main_config.yaml`. so it will give you the following prompt:

```
( bash prommt ) pysoma
no-args
1: Would you like to add an existing project?
2: Would you like to create a new project?
-------------------
Please enter the corresponding number for one of the 2 choices: 
```

After this you would likely select the second options by typing `2` and hitting `enter`.

At this point it will ask you to name the project and where it should create the project.

>NOTE: As a rule of thumb you should always avoid spaces and special characters in file and folder names with the exceptions of: `-` and `_`.

```
Please enter the corresponding number for one of the 2 choices: 2
Is <2> correct? (y/n): y
Creating a new project...
Please enter the name of the project: project_01
Is project_01 correct? (y/n): y
1: Default: Open GUI to choose path
2: Type in a path to scan
3: Use the current application directory
Select a number to choose one of the options:
```

>For option `2` you can use *relative* or *absolute* paths. In the example below I used a relative path by typing an existing directory in my project: `../testprojects/`.

```
Select a number to choose one of the options: 2
You chose: Type in a path to scan
your choice:: 2
Please type path of directory to scan: ../testprojects/
../testprojects is a directory!
```

This will create the project in that directory with the name you chose. 

