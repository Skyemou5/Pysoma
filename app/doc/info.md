# Manual

This script will initialize a project, initialize shot folders for the project, and saves out the paths to a config file that can be used in a later step.

>for per project customization make sure you do the main customization at the beginning of the project or it could break important paths that files depend on.

## Behaviour
When you run the script initially without args it will go through the initialization process in which there will be a lot of user input. After that it will check an env var to see if it's been initialized already. If it has it will read from the config and then proceed to the shot and file setup.

## Args

init -- forces initialization and runs the houdini startup

init-only -- only forces initialization

load-last -- opens last opened file (not working yet)

man -- opens manual

