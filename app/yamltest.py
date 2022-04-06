import os
import sys
import pathlib
import yaml
import pprint
import json
import ruamel.yaml
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper




if getattr(sys, 'frozen', False):
    import sys, os
    
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

def write_yaml(data):
    """ A function to write YAML file"""
    
    with open('toyaml.yml', 'w') as f:
        #yaml.dump(data, f)
        yaml.safe_dump(data, f, default_style=None, default_flow_style=False)


#yaml = yaml()

template_file = pathlib.Path(application_path)/'project_template.yml'

def read_yaml(path):
    """ A function to read YAML file"""
    result = {}
    with path.open() as f:
        config = yaml.load_all(f,Loader=yaml.FullLoader)
        for d in config:
            for k, v in d.items():
                result[k]=v
    return result


# def my_compose_document(self):
#     self.get_event()
#     node = self.compose_node(None, None)
#     self.get_event()
#     # this prevents cleaning of anchors between documents in **one stream**
#     # self.anchors = {}
#     return node

# ruamel.yaml.composer.Composer.compose_document = my_compose_document

# datas = []
# for data in ruamel.yaml.safe_load_all(template_file):
#     datas.append(data)

# datas[0]['choices']['a'] = 1
# for data in datas:
#     ruamel.yaml.round_trip_dump(data, sys.stdout, explicit_start=True)


if __name__ == "__main__":
    config = read_yaml(template_file)
    # for d in config:
    #     for k, v in d.items():
    #         test_dict[k]=v

    with open('./data.yml','w') as f:
        #f.write(json.dumps(config))
        f.write(yaml.dump(config))
    pprint.pprint(config['dir_data']['post_app_subdir_data'])
    #pprint.pprint(config)
    # with open('./log','w') as f:
    #     for k, v in config.items():
    #         f.write('%s:%s\n' % (k, v))
    # my_config = read_yaml(template_file)
    # pprint.pprint(list(my_config))
    # with open('./app/project_template.yml') as fstream:
    #     yaml_documents = yaml.load_all(fstream, Loader=yaml.FullLoader)

    #     for document in yaml_documents:
    #         for key, value in document.items():
    #             print(key, value)
    #conf_test = yaml.load(template_file,yaml.loader)
    # for i in conf_test:
    #     for k, v in i.items():
    #         print(k, '->', v)