from asyncio import subprocess
import os
import project_config_tool.lib.terminal as terminal
import pathlib
# https://github.com/skywind3000/terminal/blob/master/terminal.py

#os.system('echo $HOME')

def main():
    #print(terminal.configure.cygwin_open_bash)
    #terminal.subprocess.run('ls')
    #t = terminal.main()
    #t.ls
    #print(test)
    os.system('python ./project_config_tool/terminal.py -h')

if __name__ == "__main__":
    main()