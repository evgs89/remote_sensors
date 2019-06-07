from lib.web_server import WebInterface
import sys
import os
# from time import sleep


if sys.argv[0] != '__init__.py':
    os.chdir(os.path.dirname(sys.argv[0]))


if __name__ == '__main__':
    W = WebInterface()
