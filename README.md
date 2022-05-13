# Pre-commit Install Offline
![](https://img.shields.io/badge/python-3.8-blue)  ![](https://img.shields.io/badge/git-2.33.0-blue) ![](https://img.shields.io/badge/pip-22.0.4-blue)
## Function
Install pre-commit package offline
## Usage
First enter the directory to the script `install-offline.py`.For example, run cmd *cd /d D:\pre-commit-offline* , as the file name with path is *D:\pre-commit-offline\install-offline.py*.  

Then excute the script with command like this: 

    install-offline.py [-h] -p PACKAGE_PATH -g GIT_PATH -c CACHE_PATH
## Options
    python install-offline.py -h
    ----------------------------
    usage: install-offline.py [-h] -p PYFORMAT_PATH -g GIT_PATH -c ZIP_PATH

    Install pre-commit offline

    options:
    -h, --help            show this help message and exit
    -p PYFORMAT_PATH, --pyformat-path PYFORMAT_PATH
                        The path to the pyformat folder
    -g GIT_PATH, --Git-projects-path GIT_PATH
                        The path to the folder of a Git project
    -c ZIP_PATH, --pre-commit-cache-zip-path ZIP_PATH
                        The path to the pre-commit.zip
The three parameters are all required.
