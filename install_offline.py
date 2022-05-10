import sys
import os
import subprocess
import zipfile
import sqlite3
from sqlite3 import Error
import argparse
parser = argparse.ArgumentParser(
    description= "Install pre-commit offline"
)
parser.add_argument('-p','--python-package-path',dest='package_path',required=True)
parser.add_argument('-g','--Git-projects-path',dest='git_path',required=True)
parser.add_argument('-c','--pre-commit-cache-zip-path',dest='cache_path',required=True)
args = parser.parse_args()
if not args.package_path and args.git_path and args.cache_path:
    print("The required parameters are not complete")
    sys.exit(1)

package_path = args.p
git_path = args.g
cache_path = args.c
if sys.version[:4]!='3.8':
    raise Exception("Python version error!")
if not os.path.exists(package_path):
    raise Exception("The python package path is not exist!")
if not os.path.exists(git_path):
    raise Exception("The Git projects path is not exist!")
if not os.path.exists(cache_path):
    raise Exception("The pre-commit cache zip path is not exist!")
if not ('Git\\cmd' in os.environ['PATH']):
    raise Exception("There is no Git in the environment variables!")
command = '{}\\Scripts\\pip.exe install pre-commit'.format(sys.executable[:-11])
PIP_var = '{}\\Downloads\\pyformat'.format(os.environ['userprofile'])
subprocess.Popen(command,env={'PIP_FIND_LINKS' :  PIP_var,
                              'PIP_NO_INDEX' : 1 }   )
os.chdir(git_path)
command2 = "sys.executable[:-11]\\Scripts\\pre-commit.exe install"
subp = subprocess.Popen(command2)
if subp.poll() != 0:
    raise Exception("The subprocess exit code is not 0!")
# zip_src源文件夹
# dst_dir目标文件夹
def unzip_file(zip_src,dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src,'r')
        for file in fz.namelist():
            fz.extract(file,dst_dir)
    else:
        raise Exception("This is not zip file")
dest_dir = '{}\\.cache'.format(os.environ['userprofile'])
unzip_file(cache_path,dest_dir)
try:
    db_file = '{}\\.cache\\pre-commit\\db.db'.format(os.environ['userprofile'])
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    path1 = '{}\\.cache\\pre-commit\\repo8hglikdx' .format(os.environ['userprofile'])
    path2 = '{}\\.cache\\pre-commit\\repoemx3pt21' .format(os.environ['userprofile'])
    path3 = '{}\\.cache\\pre-commit\\repow7w1qbj0' .format(os.environ['userprofile'])
    sql1 = 'update repos set path = {} where ref = 5.10.1 '.format(path1)
    sql2 = 'update repos set path = {} where ref = 4.0.1 ' .format(path2)
    sql3 = 'update repos set path = {} where ref = 22.3.0 '.format(path3)
    cur.execute(sql1)
    cur.execute(sql2)
    cur.execute(sql3)
    conn.commit()
    cur.close()
    conn.close()
except Error as e:
    print(e)
    print("连接失败")
command3 = "{}\\Scripts\\pre-commit.exe install-hooks".format(sys.executable[:-11])
sub = subprocess.Popen(command3)
if sub.poll() != 0:
    raise Exception("The subprocess exit code is not 0!")

