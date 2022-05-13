# Pre-commit Install Offline
![](https://img.shields.io/badge/python-3.8-blue)  ![](https://img.shields.io/badge/git-2.33.0-blue) ![](https://img.shields.io/badge/pip-22.0.4-blue)
## Function
Install pre-commit package offline
## Options
    python install-offline.py -h
    ----------------------------
    usage: install-offline.py [-h] -p PACKAGE_PATH -g GIT_PATH -c CACHE_PATH

    Install pre-commit offline

    options:
      -h, --help            show this help message and exit
      -p PACKAGE_PATH, --pyformat-path PACKAGE_PATH
                        The path to the pyformat folder
      -g GIT_PATH, --Git-projects-path GIT_PATH
                        The path to the folder of a Git project
      -c CACHE_PATH, --pre-commit-cache-zip-path CACHE_PATH
                        The path to the pre-commit.zip
The three parameters are all required.
