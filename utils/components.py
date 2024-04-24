import hashlib
import os


def find_files(fname): 
    r"""
    Finds all files in a directory (including subdirectories) and returns them.
    Example: ['C:\Users\User\Downloads\PROJECT\Dani', 'C:\Users\User\Downloads\PROJECT\Dani\Chapter 1.docx']
    """
    if os.path.isdir(fname):
        list_files = os.listdir(fname)
        all_files = list()
        for i in list_files:
            fullpath = os.path.join(fname, i)
            if os.path.isdir(fullpath):
                all_files = all_files + find_files(fullpath)
            else:
                all_files.append(fullpath)
        return all_files
    elif os.path.isfile(fname):
        return list(fname.split(" "))
    
    
def generate_md5(fname):
    r"""
    Generates an MD5 hash for each file found by the find_files() function
    and returns a list containing all hash data.
    Example: ['C:\Users\User\Downloads\PROJECT\Dani', 'C:\Users\User\Downloads\PROJECT\Dani\Chapter 1.docx']
             ['dfdfjhkjhfa1fdsgdg', 'kjhjdhfi8eseoidfjdf']
    """
    hash_data = [] 
    for i in range(len(fname)):
        with open(fname[i], "rb") as f:
            data = f.read()
            md5 = hashlib.md5()
            md5.update(data)
            md5_hash = md5.hexdigest()
            hash_data.append(md5_hash)
    return hash_data


def create_hashfile(directory_path, x, y):
    """
    Takes two parameters x = latest log and y = new log.
    Creates two .txt files and stores x in a file named hash_data_1.txt
    and another .txt file named hash_data_0.txt.
    """
    # Replace '/' and '\' characters in directory_path with '_'
    filename = directory_path.replace('/', '_').replace('\\', '_')
    
    if os.path.exists(f"{filename}_1.txt") and os.path.exists(f"{filename}_0.txt"):
        os.remove(f"{filename}_1.txt")
        os.rename(f"{filename}_0.txt", f"{filename}_1.txt")
    i = 1
    while os.path.exists(f"{filename}_{i}.txt"):
        i -= 1
    hash_file = open(f"{filename}_{i}.txt", "a+")
    for i in range(len(x)):
        hash_file.write(x[i])
        hash_file.write("\t")
        hash_file.write(y[i])
        hash_file.write("\n")

    hash_file.close()
    
def read_file(fname): 
    r"""
    Reads file_name and returns a dictionary with files and their MD5 hashes.
    Example: {
               'C:\Users\User\Downloads\PROJECT\Dani': 'dfdfjhkjhfa1fdsgdg',
               'C:\Users\User\Downloads\PROJECT\Dani\Chapter 1.docx': 'kjhjdhfi8eseoidfjdf',
             }
    """
    file_dict = {}
    with open(fname, "r") as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                key, value = parts
                file_dict[key] = value
            else:
                print(f"Ignoring invalid line: {line}")
    return file_dict


def changed_files(old_dict, new_dict):
    r"""
    Takes two parameters old_dict = hash_data_1.txt in the form of a dictionary
                        and new_dict = hash_data_0.txt in the form of a dictionary
    Returns a list of all files that have changed.
    Example: ['C:\Users\User\Downloads\PROJECT\Dani', 'C:\Users\User\Downloads\PROJECT\Dani\Chapter 1.docx']
    """
    changed_list = []
    for i in old_dict.keys():
        if i in new_dict.keys():
            if old_dict[i] not in new_dict.values():
                changed_list.append(i)
    return changed_list


def deleted_files(old_dict, new_dict):
    r"""
    Takes two parameters old_dict = hash_data_1.txt in the form of a dictionary
                        and new_dict = hash_data_0.txt in the form of a dictionary
    Returns a list of all files that have been deleted.
    Example: ['C:\Users\User\Downloads\PROJECT\Dani', 'C:\Users\User\Downloads\PROJECT\Dani\Chapter 1.docx']
    """
    removed_files = list(filter(lambda x: x not in new_dict, old_dict))
    return removed_files

def new_files(old_dict, new_dict):
    r"""
    Takes two parameters old_dict = hash_data_1.txt in the form of a dictionary
                        and new_dict = hash_data_0.txt in the form of a dictionary
    Returns a list of all files that have been created.
    Example: ['C:\Users\User\Downloads\PROJECT\Dani', 'C:\Users\User\Downloads\PROJECT\Dani\Chapter 1.docx']
    """
    added_files = list(filter(lambda x: x not in old_dict, new_dict))
    return added_files