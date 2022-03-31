"""
gives relative root a new 'shots/shot_n' directory with each program invocation,
where 'n' is an incrementing number value
"""

from pathlib import Path
import os


subdir_names = [
    "GEO",
    "HIP",
    "RENDER",
    "TEXTURE",
    "BLEND",
    "ASSETS"
]


def create_shot():
    #ensure top-level 'shots' exists
    top_level_shot = Path("./shots")
    if not Path.is_dir(top_level_shot):
        Path.mkdir(top_level_shot)

    #case 1 - creating first shot directory
    first_shot_n = Path("./shots/Shot_1")
    if not Path.is_dir(first_shot_n):
        Path.mkdir(first_shot_n)
        create_resource_subdirs(first_shot_n)
        print(f"\'{first_shot_n}\' created along with resource dirs.")
    #case 2 - creating any subsequent shot directory
    else:
        shot_n = first_shot_n
        #skip existing shot directories...
        while Path.is_dir(shot_n):
            try:
                incremented_number = int(shot_n.parts[1].split('_')[1])+1
                updated_shot_n = shot_n.parts[1].replace(shot_n.parts[1].split('_')[1],str(incremented_number))
                shot_n = Path.joinpath(Path(shot_n.parts[0]), Path(updated_shot_n))
            except:
                raise Exception("couldn't increment appended folder number")

        #make the new shot directory...
        Path.mkdir(shot_n)

        #create resources for the new shot directory
        create_resource_subdirs(shot_n)
        #get paths for all resource directories
        resource_paths = get_resource_paths(shot_n)
        #write paths to 'temp_paths.txt'
        write_to_temp(resource_paths)
        #load resources to local 'ENV'
        load_env_resource_vars(resource_paths)

        #DOES user want to open new shot folder?
        user_choice = input(
            f"\'{shot_n.stem}\' created along with resource dirs." +
            "Do you want to open the new shot folder? y/n: ").lower()
        if user_choice == 'y':
            os.chdir(shot_n)
            print(f"changed shell dir to \'{shot_n.stem}\'")


def create_resource_subdirs(curr_path):
    #create all conventional subdirs for a given (sub)directory
    for item in subdir_names:
        resource_path = Path.joinpath(curr_path,Path(f"{item}"))
        if not Path.is_dir(resource_path):
            os.mkdir(resource_path)


def write_to_temp(i_stream):
    with open("temp_paths.txt", 'w') as f_stream:
        f_stream.writelines(i+'\n' if i_stream.index(i) + 1 !=
                    len(i_stream) else i for i in i_stream)


def load_env_resource_vars(paths):
    for item in paths:
        f_name = Path(item).stem.strip(' ')
        os.environ[f_name] = item


def get_resource_paths(curr_path):
    resource_paths = [i[0] for i in os.walk(
        curr_path) if os.path.basename(str(i[0])) in subdir_names]
    return resource_paths


if __name__ == '__main__':
    create_shot()