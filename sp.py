import platform
import subprocess


def is_windows() -> bool:
    return platform.system().lower() == "windows"


def execute(command: str, env: dict = {}, cwd: str = "C:\\Windows\\Temp" if is_windows() else "/dev/shm") -> str:
    args = {
        "stderr": subprocess.PIPE,
        "stdout": subprocess.PIPE,
        "encoding": "cp866" if is_windows() else "utf-8",
        "cwd": cwd,
        "shell": True
    }
    if len(env.keys()):
        args["env"] = env

    process = subprocess.Popen(command, **args)
    res, err = process.communicate()
    return ''.join([res, err])


# print(execute("whoami"))
