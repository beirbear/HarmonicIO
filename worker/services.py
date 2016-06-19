import os.path
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Services(object):

    """
    Service method, check for file exist in the local machine
    """
    @staticmethod
    def is_file_exist(file):
        return os.path.exists(file)

    @staticmethod
    def t_print(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
        exit()

    @staticmethod
    def e_print(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
