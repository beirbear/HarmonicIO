import os.path
import sys


class Services(object):

    """
    Service method, check for file exist in the local machine
    """
    @staticmethod
    def is_file_exist(file):
        return os.path.exists(file)

    @staticmethod
    def is_folder_exist(folder):
        return os.path.isdir(folder)

    @staticmethod
    def t_print(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
        exit()

    @staticmethod
    def e_print(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
