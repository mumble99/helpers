import os


def path_exists(path: str) -> bool:
    return os.path.exists(path)


def is_file(file_path: str) -> bool:
    return os.path.isfile(file_path)


def is_directory(dir_path: str) -> bool:
    return os.path.isdir(dir_path)


def file_exists(file_path: str) -> bool:
    return path_exists(file_path) and is_file(file_path)


def directory_exists(dir_path: str) -> bool:
    return path_exists(dir_path) and is_directory(dir_path)


def rename(file_path: str, new_file_name: str) -> bool:
    if path_exists(file_path):
        basename = os.path.basename(file_path)
        try:
            os.rename(file_path, file_path.replace(basename, new_file_name))
            return True
        except PermissionError:
            return False
    return False


def create_dir(dir_name: str) -> bool:
    try:
        os.makedirs(dir_name)
        return True
    except FileExistsError:
        return True
    except OSError:
        return False


def get_absolute_path(path: str) -> str:
    if path_exists(path):
        return os.path.abspath(path)
    return ""


def list_dir(dir_path: str) -> list:
    all_content = []
    if is_directory(dir_path):
        abs_path = get_absolute_path(dir_path)
        for root, subdirs, files in os.walk(abs_path):
            for subdir in subdirs:
                all_content.append(get_absolute_path("%s/%s" % (root, subdir)))
            for file in files:
                all_content.append(get_absolute_path("%s/%s" % (root, file)))
    return all_content


def delete(path: str) -> bool:
    try:
        if is_file(path):
            os.unlink(path)
            return True
        elif is_directory(path):
            files_in_dir = list_dir(path)
            for f in files_in_dir:
                delete(f)
            os.rmdir(path)
            return True
        return False
    except OSError:
        return False


def read_file(file_path: str, mode: str = "r") -> str or bytes:
    if file_exists(file_path):
        f = open(file_path, mode=mode)
        content = f.read()
        f.close()
        return content
    return "" if "b" not in mode else b""


def write_file(file_path: str, data: str or bytes, mode: str = "w") -> bool:
    try:
        with open(file_path, mode=mode) as f:
            f.write(data)
            return True
    except OSError:
        return False


# print(rename("temp", "new-temp"))
# print(write_file("new-temp/t2.txt", b"xd", mode="ab"))
# print(read_file("new-temp/t.txt", mode="rb"))
# print(delete("new-temp/t.txt"))
# print(delete("new-temp"))
# print(list_dir("new-temp"))
# print(get_absolute_path("new-temp"))
# for fp in list_dir("new-temp"):
#     print(fp, read_file(fp))
# delete("new-temp")
# print(create_dir("test"))
