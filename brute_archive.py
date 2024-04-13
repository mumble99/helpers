import os
import argparse
import sys
import datetime


def get_type_of_archive(filepath):
    basename = os.path.basename(filepath)
    ext = basename.split(".")[-1]
    return {
        "zip": "zip",
        "rar": "rar",
        "7z": "7z"
    }.get(ext)


def unsupported_arch(_, __):
    print("this archive not supported")
    sys.exit(1)


def print_res(start_time, count, password, success):
    stop_time = datetime.datetime.now()
    if success:
        print("the archive was brute forced in %d attempts in %s seconds and has a password of %s" % (
            count, (stop_time - start_time).seconds, password)
              )
    else:
        print("failed to guess the password for the archive. time spent %s seconds. attempts - %d" % (
            (stop_time - start_time).seconds, count)
              )
    sys.exit(0)


def file_exists(filepath):
    return os.path.exists(filepath) and os.path.isfile(filepath)


def read_wordlist(filepath):
    with open(filepath) as f:
        return f.read().split("\n")


def brute_zip(filepath, wordlist_path):
    import zipfile
    wordlist = read_wordlist(wordlist_path)
    count = 0
    start_time = datetime.datetime.now()
    with zipfile.ZipFile(filepath) as zfile:
        for pwd in wordlist:
            try:
                zfile.extractall(path='/tmp', pwd=pwd.strip().encode())
                print_res(start_time, count, pwd.strip(), True)
            except RuntimeError:
                count += 1
    print_res(start_time, count, "", False)


def brute_rar(filepath, wordlist_path):
    try:
        import rarfile
    except ImportError:
        sys.exit("cannot import rarfile. pls install manually.\npip3 install rarfile")
    wordlist = read_wordlist(wordlist_path)
    count = 0
    start_time = datetime.datetime.now()
    with rarfile.RarFile(filepath) as zfile:
        for pwd in wordlist:
            try:
                zfile.extractall(path="/tmp", pwd=pwd.strip())
                print_res(start_time, count, pwd.strip(), True)
            except Exception:
                count += 1
    print_res(start_time, count, "", False)


def brute_7z(filepath, wordlist_path):
    try:
        import py7zr
    except ImportError:
        sys.exit("cannot import py7zr. pls install manually.\npip3 install py7zr")
    wordlist = read_wordlist(wordlist_path)
    count = 0
    start_time = datetime.datetime.now()
    for pwd in wordlist:
        try:
            with py7zr.SevenZipFile(filepath, 'r', password=pwd.strip()) as zfile:
                zfile.extractall("/tmp")
                print_res(start_time, count, pwd, True)
        except Exception:
            count += 1
    print_res(start_time, count, "", False)


def main():
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument("-a", "--archive", help="archive path")
    parser.add_argument("-w", "--wordlist", help="wordlist path")
    args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    archive_path = args.archive
    wordlist_path = args.wordlist
    for f in [archive_path, wordlist_path]:
        if not file_exists(f):
            print("%s does not exists" % f)
            sys.exit(1)
    mapping = {
        "zip": brute_zip,
        "rar": brute_rar,
        "7z": brute_7z,
        None: unsupported_arch
    }
    mapping.get(get_type_of_archive(archive_path))(archive_path, wordlist_path)


if __name__ == "__main__":
    main()
