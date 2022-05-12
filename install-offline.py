import sys
import os
import subprocess
import zipfile
import sqlite3
from sqlite3 import Error
import argparse

cache_dir = os.environ["userprofile"]
sys_path = sys.executable


def dir_exist(path):
    """Check whether the path exists"""
    if not os.path.exists(path):
        print(f"The {path} does not exist!")
        sys.exit(1)
    print("The path exists")


def run_cmd(command, **kwargs):
    """Set environment variables, run the command"""
    sub = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs,
    )
    val = sub.communicate()
    ret = sub.wait()
    return (ret, val)


def unzip_file(zip_src, dst_dir):
    """Unzip file to the destination path"""
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, "r")
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        print("Unzip successfully.")
    else:
        print("This is not a zip file")
        sys.exit(-1)
    return


def cli():
    parser = argparse.ArgumentParser(description="Install pre-commit offline")
    parser.add_argument(
        "-p", "--python-package-path", dest="package_path", required=True
    )
    parser.add_argument(
        "-g", "--Git-projects-path", dest="git_path", required=True
    )
    parser.add_argument(
        "-c", "--pre-commit-cache-zip-path", dest="cache_path", required=True
    )
    args = parser.parse_args()
    if not (args.package_path and args.git_path and args.cache_path):
        print("The required parameters are not complete")
        sys.exit(1)
    package_path = args.package_path
    print('package_path:',package_path)
    git_path = args.git_path
    print('git_path:',git_path)
    cache_path = args.cache_path
    print('cache_path:',cache_path)
    envs = {"PIP_FIND_LINKS": package_path, "PIP_NO_INDEX": "1"}

    if sys.version[:3] != "3.8":
        print("Python version error!")
        sys.exit(1)
    else:
        print('Python version right.')

    dir_exist(package_path)

    dir_exist(git_path)

    dir_exist(cache_path)

    check_git_cmd = "git --version"

    if run_cmd(check_git_cmd, env=envs)[0] != 0:
        print("Environment variables do not contain Git!")
        sys.exit(1)
    else:
        print("Environment variables contain Git.")

    pip_install_cmd = f"{sys_path} -m pip install pre-commit"

    if run_cmd(pip_install_cmd, env=envs)[0] != 0:
        print("pip install failed!")
        sys.exit(1)
    else:
        print("pip install successfully.")

    install_cmd = f"{sys_path} -m pre_commit install"

    if run_cmd(install_cmd, env=envs)[0] != 0:
        print("pre_commit install failed!")
        sys.exit(1)
    else:
        print("pre-commit install successfully.")

    dest_dir = f"{cache_dir}\\.cache"
    unzip_file(cache_path, dest_dir)  # zip_src = cache_path

    try:
        db_file = f"{dest_dir}\\pre-commit\\db.db"
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        path1 = f"{cache_dir}\\.cache\\pre-commit\\repo8hglikdx"
        path2 = f"{cache_dir}\\.cache\\pre-commit\\repoemx3pt21"
        path3 = f"{cache_dir}\\.cache\\pre-commit\\repow7w1qbj0"
        sql1 = f"update repos set path = '{path1}' where repo = 'https://github.com/PyCQA/isort' "
        sql2 = f"update repos set path = '{path2}' where repo = 'https://github.com/PyCQA/flake8' "
        sql3 = f"update repos set path = '{path3}' where repo = 'https://github.com/psf/black' "

        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)

        conn.commit()
        cur.close()
        conn.close()

    except Error as e:
        print(e)
        print("Connect false!")

    hooks_cmd = f"{sys_path} -m pre_commit install-hooks"
    if run_cmd(hooks_cmd, env=envs)[0] != 0:
        print("pre_commit install-hooks failed!")
        sys.exit(1)
    else:
        print('pre-commit install-hooks successfully.')

    print("Pre-commit has been installed offline successfully!")


cli()
