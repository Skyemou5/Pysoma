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


