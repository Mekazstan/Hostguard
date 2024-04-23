import os
import hashlib
def find_files(fname): 
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
    hash_data = [] 
    for i in range(len(fname)):
        with open(fname[i], "rb") as f:
            data = f.read()
            md5 = hashlib.md5()
            md5.update(data)
            md5_hash = md5.hexdigest()
            hash_data.append(md5_hash)
    return hash_data
def create_hashfile(x, y):
    if os.path.exists("hash_data_1.txt") and os.path.exists("hash_data_0.txt"):
        os.remove("hash_data_1.txt")
        os.rename("hash_data_0.txt", "hash_data_1.txt")
    i = 1
    while os.path.exists(f"hash_data_{i}.txt"):
        i -= 1
    hash_file = open(f"hash_data_{i}.txt", "a+")
    for i in range(len(x)):
        hash_file.write(x[i])
        hash_file.write("\t")
        hash_file.write(y[i])
        hash_file.write("\n")

    hash_file.close()
def read_file(fname): 
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
    changed_list = []
    for i in old_dict.keys():
        if i in new_dict.keys():
            if old_dict[i] not in new_dict.values():
                changed_list.append(i)
    return changed_list
def deleted_files(old_dict, new_dict):
    removed_files = list(filter(lambda x: x not in new_dict, old_dict))
    return removed_files

def new_files(old_dict, new_dict):
    added_files = list(filter(lambda x: x not in old_dict, new_dict))
    return added_files



def main():
    print("Welcome to Intrusion Detection Check")
    i = True
    while i:
        the_path = input("What folder (path full or relative) do you want to protect?\n")
        print(find_files(the_path))
        if os.path.isdir(the_path) or os.path.isfile(the_path):
            var_find_files = find_files(the_path)
            var_generate_md5 = generate_md5(var_find_files)
            create_hashfile(var_find_files, var_generate_md5)
            if os.path.exists("hash_data_0.txt") and os.path.exists("hash_data_1.txt"):
                old_file = read_file("hash_data_1.txt")
                new_file = read_file("hash_data_0.txt")
                var_changed_files = changed_files(old_file, new_file)
                var_deleted_files = deleted_files(old_file, new_file)
                var_new_files = new_files(old_file, new_file)
                print("Report")
                print("------")
                if var_changed_files == [] and var_deleted_files == [] and var_new_files == []:
                    print("There where no changes in the folder")
                else:
                    print("WARNING!\n")
                    print("NEW FILES")
                    for i in var_new_files:
                        print(i)
                    print("\n")
                    print("CHANGED FILES")
                    for i in var_changed_files:
                        print(i)
                    print("\n")
                    print("REMOVED FILES")
                    for i in var_deleted_files:
                        print(i)
            else:
                print("The program is ready for...") 
            i = False
        else:
            print(the_path, "does not exists! Try again!")
if __name__ == "__main__":
    main()

