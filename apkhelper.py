import os
import subprocess
import binascii
import sys
import zipfile
import argparse

APK_TOOL_URL = "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar"
BUILD_TOOL_URL = "https://dl.google.com/android/repository/build-tools_r33-linux.zip"
APKTOOL_BASH_WRAPPER = "IyEvYmluL2Jhc2gKCnByb2c9IiQwIgp3aGlsZSBbIC1oICIke3Byb2d9IiBdOyBkbwogICAgbmV3UHJvZz1gL2Jpbi9scyAtbGQgIiR7cHJvZ30iYAoKICAgIG5ld1Byb2c9YGV4cHIgIiR7bmV3UHJvZ30iIDogIi4qIC0+IFwoLipcKSQiYAogICAgaWYgZXhwciAieCR7bmV3UHJvZ30iIDogJ3gvJyA+L2Rldi9udWxsOyB0aGVuCiAgICAgICAgcHJvZz0iJHtuZXdQcm9nfSIKICAgIGVsc2UKICAgICAgICBwcm9nZGlyPWBkaXJuYW1lICIke3Byb2d9ImAKICAgICAgICBwcm9nPSIke3Byb2dkaXJ9LyR7bmV3UHJvZ30iCiAgICBmaQpkb25lCm9sZHdkPWBwd2RgCnByb2dkaXI9YGRpcm5hbWUgIiR7cHJvZ30iYApjZCAiJHtwcm9nZGlyfSIKcHJvZ2Rpcj1gcHdkYApwcm9nPSIke3Byb2dkaXJ9Ii9gYmFzZW5hbWUgIiR7cHJvZ30iYApjZCAiJHtvbGR3ZH0iCgpqYXJmaWxlPWFwa3Rvb2wuamFyCmxpYmRpcj0iJHByb2dkaXIiCmlmIFsgISAtciAiJGxpYmRpci8kamFyZmlsZSIgXQp0aGVuCiAgICBlY2hvIGBiYXNlbmFtZSAiJHByb2ciYCI6IGNhbid0IGZpbmQgJGphcmZpbGUiCiAgICBleGl0IDEKZmkKCmphdmFPcHRzPSIiCgojIElmIHlvdSB3YW50IERYIHRvIGhhdmUgbW9yZSBtZW1vcnkgd2hlbiBleGVjdXRpbmcsIHVuY29tbWVudCB0aGUgZm9sbG93aW5nCiMgbGluZSBhbmQgYWRqdXN0IHRoZSB2YWx1ZSBhY2NvcmRpbmdseS4gVXNlICJqYXZhIC1YIiBmb3IgYSBsaXN0IG9mIG9wdGlvbnMKIyB5b3UgY2FuIHBhc3MgaGVyZS4KIwpqYXZhT3B0cz0iLVhteDEwMjRNIC1EZmlsZS5lbmNvZGluZz11dGYtOCAtRGpkay51dGlsLnppcC5kaXNhYmxlWmlwNjRFeHRyYUZpZWxkVmFsaWRhdGlvbj10cnVlIC1EamRrLm5pby56aXBmcy5hbGxvd0RvdFppcEVudHJ5PXRydWUiCgojIEFsdGVybmF0aXZlbHksIHRoaXMgd2lsbCBleHRyYWN0IGFueSBwYXJhbWV0ZXIgIi1KeHh4IiBmcm9tIHRoZSBjb21tYW5kIGxpbmUKIyBhbmQgcGFzcyB0aGVtIHRvIEphdmEgKGluc3RlYWQgb2YgdG8gZHgpLiBUaGlzIG1ha2VzIGl0IHBvc3NpYmxlIGZvciB5b3UgdG8KIyBhZGQgYSBjb21tYW5kLWxpbmUgcGFyYW1ldGVyIHN1Y2ggYXMgIi1KWG14MjU2TSIgaW4geW91ciBhbnQgc2NyaXB0cywgZm9yCiMgZXhhbXBsZS4Kd2hpbGUgZXhwciAieCQxIiA6ICd4LUonID4vZGV2L251bGw7IGRvCiAgICBvcHQ9YGV4cHIgIiQxIiA6ICctSlwoLipcKSdgCiAgICBqYXZhT3B0cz0iJHtqYXZhT3B0c30gLSR7b3B0fSIKICAgIHNoaWZ0CmRvbmUKCmlmIFsgIiRPU1RZUEUiID0gImN5Z3dpbiIgXSA7IHRoZW4KCWphcnBhdGg9YGN5Z3BhdGggLXcgICIkbGliZGlyLyRqYXJmaWxlImAKZWxzZQoJamFycGF0aD0iJGxpYmRpci8kamFyZmlsZSIKZmkKCiMgYWRkIGN1cnJlbnQgbG9jYXRpb24gdG8gcGF0aCBmb3IgYWFwdApQQVRIPSRQQVRIOmBwd2RgOwpleHBvcnQgUEFUSDsKZXhlYyBqYXZhICRqYXZhT3B0cyAtamFyICIkamFycGF0aCIgIiRAIgo="
TOOLS = [
    {"name": "apktool", "path": "/usr/local/bin/apktool"},
    {"name": "apktool.jar", "path": "/usr/local/bin/apktool.jar"},
    {"name": "buildapp", "path": "/usr/local/bin/buildapp"},
    {"name": "zipalign", "path": "/usr/local/bin/android/zipalign"},
    {"name": "keytool", "path": "/usr/bin/keytool"},
    {"name": "apksigner", "path": "/usr/local/bin/android/apksigner"}
]
DEFAULT_KEYSTORE_NAME = "default.keystore"
DEFAULT_KEYSTORE_ALIAS = "default"
TEMPLATE_CREATE_KEYSTORE = r'echo "123456\n123456\nFN\nOU\nO\nC\nS\nCC\nyes\n" | keytool -genkey -v -keystore %s -alias %s -keyalg RSA -keysize 2048 -validity 10000' % (
    DEFAULT_KEYSTORE_NAME, DEFAULT_KEYSTORE_ALIAS
)
TEMPLATE_UNPACK_APK = "apktool d %s -o %s"
TEMPLATE_BUILD_APK = (r'echo "%s\n123456\n" | ' % DEFAULT_KEYSTORE_ALIAS) + 'buildapp -d %s -o %s -k %s'


def extract_zip(zip_path: str, dst_path: str):
    tmp_path = "/tmp/android/"
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(tmp_path)
    child_folder = os.listdir(tmp_path)[0]
    execute("mv %s %s" % (tmp_path + child_folder, dst_path))
    execute("rm -rf %s" % tmp_path)


def b64_decode(b64string: str) -> str:
    return binascii.a2b_base64(b64string).decode()


def tool_exists(tool: str) -> bool:
    return 0 == execute("command -v %s" % tool)[0]


def execute(command: str) -> tuple:
    process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    res, err = process.communicate()
    return process.returncode, ''.join([res.decode(), err.decode()])


def make_executable(path: str) -> bool:
    return 0 == execute("chmod +x %s" % path)[0]


def download_file(url: str, dst_path: str) -> bool:
    return 0 == execute("curl -L %s -o %s" % (url, dst_path))[0]


def write_file(file_path: str, data: str or bytes, mode: str = "w") -> bool:
    try:
        with open(file_path, mode=mode) as f:
            f.write(data)
            return True
    except OSError:
        return False


def update_env_path_command(path: str):
    print('export PATH="$PATH:%s"' % path)


def install_apktool() -> bool:
    wrapper = b64_decode(APKTOOL_BASH_WRAPPER)
    if not write_file(TOOLS[0]["path"], wrapper):
        return False
    if not download_file(APK_TOOL_URL, TOOLS[1]["path"]):
        return False
    return True


def install_buildapp() -> bool:
    if execute("pip3 install buildapp --upgrade && buildapp_fetch_tools")[0] == 0:
        return True
    return False


def install_buildtools() -> bool:
    tmp_zip_file_path = "/tmp/android.zip"
    extract_path = "/usr/local/bin/android"
    if not download_file(BUILD_TOOL_URL, tmp_zip_file_path):
        return False
    extract_zip(tmp_zip_file_path, extract_path)
    execute("rm %s" % tmp_zip_file_path)
    update_env_path_command(extract_path)
    print("please update your $PATH in /etc/environment\nAdd %s" % extract_path)
    return True


def install_dependencies() -> bool:
    if not install_buildapp():
        return False
    if not install_apktool():
        return False
    if not install_buildtools():
        return False
    for tool in TOOLS:
        make_executable(tool["path"])
    return True


def execute_command_wrapper(command: str) -> bool:
    status, res = execute(command)
    if status == 0:
        return True
    print("Something went wrong")
    print(res)
    return False


def check_dependencies() -> bool:
    for tool in TOOLS:
        if not tool_exists(tool["name"]):
            print("cannot find tool %s" % tool)
            return False
    return True


def main():
    if os.getuid() != 0:
        sys.exit("please run as root")
    parser = argparse.ArgumentParser(prog="apkhelper.py")
    parser.add_argument("-i", "--install", help="install dependencies", action="store_true")
    parser.add_argument("-u", "--unpack", help="unpack apk file", action="store_true")
    parser.add_argument("-b", "--build", help="build apk file", action="store_true")
    parser.add_argument("-g", "--generate", help="generate keystore", action="store_true")
    parser.add_argument("-a", "--apk", help="apkfile path")
    parser.add_argument("-s", "--source", help="sourcefile path")
    parser.add_argument("-o", "--output", help="source output path")
    args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    if args.install:
        if install_dependencies():
            print("dependencies successfully installed")
        else:
            print("error while install dependencies")
        sys.exit(0)

    if not check_dependencies():
        print("could not find dependencies, please install dependencies manually, or run the script with the -i option")
        sys.exit(1)

    if args.generate:
        print("execute %s" % TEMPLATE_CREATE_KEYSTORE)
        if execute_command_wrapper(TEMPLATE_CREATE_KEYSTORE):
            print("keystore with name %s and alias %s created" % (DEFAULT_KEYSTORE_NAME, DEFAULT_KEYSTORE_ALIAS))
            sys.exit(0)
        sys.exit(1)
    if args.build:
        if not args.source or not args.apk:
            print("-s and -a has been set")
            sys.exit(1)
        command = TEMPLATE_BUILD_APK % (args.source, args.apk, DEFAULT_KEYSTORE_NAME)
        print("execute %s" % command)
        if execute_command_wrapper(command):
            sys.exit(0)
        sys.exit(1)
    if args.unpack:
        if not args.output or not args.apk:
            print("-a and -o has been set")
            sys.exit(1)
        command = TEMPLATE_UNPACK_APK % (args.apk, args.output)
        print("execute %s" % command)
        if execute_command_wrapper(command):
            sys.exit(0)
        sys.exit(1)


if __name__ == "__main__":
    main()
