import pathlib
import os
import collections

#print(pathlib.Path(__file__).parents[1])

# def smart_divide(func):
#     def inner(a, b):
#         print("I am going to divide", a, "and", b)
#         if b == 0:
#             print("Whoops! cannot divide")
#             return

#         return func(a, b)
#     return inner


# @smart_divide
# def divide(a, b):
#     print(a/b)

# divide(3,2)

testdict = {
    'users': {
        'user': ''
    }   
}

userdict = {
    'name':'user',

}



def user_data_constructor(func):
    def inner(user_name):
        projectdata = {
            'users':''
        }
        userdata = {'name':user_name}
        projectdata['users']=user_name
        print(projectdata)




def project_settings_file_dec(func):
    # config stuff
    #fp = pathlib.Path(filepath)/'.projectdata.yaml'
    def inner(fp):

        try:
            return(func)
            #print('project config exists...')
            if is_file_empty(fp):
                print('file is empty...')
                
            else:
                print('file is not empty...')
            #pathlib.Path(fp).exists()

            #fp.open('w',encoding='utf-8')

        except FileNotFoundError:
            print('creating project config file...')
            fp.open("w",encoding="utf-8")
            
            inner(fp)
    return inner

@ user_data_constructor
@ project_settings_file_dec
def read_write_project_data(func):
    def inner(fp,dict):
        pass

testfile = pathlib.Path(pathlib.Path.cwd())/'test.yaml'


# class Template:
#     def __init__(self,users,user,role) -> None:
#         self.users = {}
#         self.user = user
#         self.role = role
#     def construct
#     def __str__(self):
#         pass

# print(Template(testdict))

name = 'ben'
userdata = {}

@ read_write_project_data
def init_data(fp,dict,name):
    pass


def main():
    init_data(testfile,userdata,name)