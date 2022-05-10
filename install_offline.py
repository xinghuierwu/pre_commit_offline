import sys
import os
import subprocess
import zipfile
import sqlite3
from sqlite3 import Error
import argparse
cache_dir = os.environ['userprofile']
def dir_exist(path):
    '''Check whether the path exists'''
    if not os.path.exists(path):
        print(f'The {path} does not exist!')
        sys.exit(1)
    print('The path exists')

def IsGitEnv():
    '''Check whether Git is in the environment variables'''
    p = subprocess.Popen('where git',
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, )
    if 'git' not in str(p.communicate()[0]):
        print("No Git in the environment variables!")
        sys.exit(-1)
    print("Git is in the environment variables.")
    return

def SetEnv(package_path):
    '''Set the environment variables and run the command to install package'''
    command = f'{sys.executable} -m pip install pre-commit'
    sub = subprocess.Popen( command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            env={
                                'PIP_FIND_LINKS': package_path,
                                'PIP_NO_INDEX': '1'
                            })
    ret = sub.wait()
    if ret != 0:
        print('The return code of the subprocess is not 0!')
        sys.exit(1)
    return

def RunCmd(command):
    '''Run the command and check the return code'''
    sub = subprocess.Popen(command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    ret = sub.wait()
    if ret != 0:
        print('The return code of the subprocess is not 0!')
        sys.exit(1)

def unzip_file(zip_src, dst_dir):
    '''Unzip file to the destination path'''
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print("This is not a zip file")
        sys.exit(-1)
    return
def cli():
    parser = argparse.ArgumentParser(
        description="Install pre-commit offline"
    )
    parser.add_argument('-p', '--python-package-path', dest='package_path', required=True)
    parser.add_argument('-g', '--Git-projects-path', dest='git_path', required=True)
    parser.add_argument('-c', '--pre-commit-cache-zip-path', dest='', required=True)
    args = parser.parse_args()
    if not (args.package_path and args.git_path and args.cache_path):
        print("The required parameters are not complete")
        sys.exit(1)
    package_path = args.package_path
    git_path = args.git_path
    cache_path = args.cache_path
    if sys.version[:4] != '3.8':
        print("Python version error!")
        sys.exit(1)
    dir_exist(package_path)
    dir_exist(git_path)
    dir_exist(cache_path)
    IsGitEnv()
    SetEnv(package_path)
    install_cmd = f'{sys.executable} -m pre_commit install'
    RunCmd(install_cmd)
    dest_dir = f'{cache_dir}\\.cache'
    unzip_file(cache_path,dest_dir) #zip_src = cache_path
    try:
        db_file = 'D:\\pre-commit\\db.db'
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        path1 = f'{cache_dir}\\.cache\\pre-commit\\repo8hglikdx'
        path2 = f'{cache_dir}\\.cache\\pre-commit\\repoemx3pt21'
        path3 = f'{cache_dir}\\.cache\\pre-commit\\repow7w1qbj0'
        sql1 = f"update repos set path = '{path1}' where ref = '5.10.1' "
        sql2 = f"update repos set path = '{path2}' where ref = '4.0.1' "
        sql3 = f"update repos set path = '{path3}' where ref = '22.3.0' "
        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)
        conn.commit()
        cur.close()
        conn.close()
    except Error as e:
        print(e)
        print("Connect false!")
    hooks_cmd = f'{sys.executable} -m pre_commit install-hooks'
    RunCmd(hooks_cmd)
    print('Pre-commit has been installed offline successfully!')
cli()

