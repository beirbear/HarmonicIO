from abc import ABCMeta, abstractmethod
from .services import Services


class DataSource(metaclass=ABCMeta):
    """
    This is ab an abstract that wrap the inherited data sources, (Local, Swift Bucket, Actual Simulation).
    """
    @abstractmethod
    def get_data(self, byte_object, file_idx):
        pass


class LocalFileDataSource(DataSource):
    """
    This class use data from local files as data source.
    -----------------------------------------------------------------------------------------
    CAUTION: The implementation of method in this class doesn't prevent from race condition.
    We implement this way because we rely on Thread in Python that is controlled by GIL.
    When, you change from Thread to Process Pool. You must implement some kind of lock to
    make the synchronization correct.
    -----------------------------------------------------------------------------------------
    """

    def __init__(self, source_folder='/', file_extension='*'):
        # Check that folder is exist or not, if not throw exception
        if not Services.is_folder_exist(source_folder):
            Services.t_print("{0} does not exist!".format(source_folder))

        if source_folder[-1] != '/':
            source_folder += '/'

        import glob
        self.__source_files = glob.glob(source_folder + '*.' + file_extension)
        self.__source_folder = source_folder
        self.__index = 0

        print("{0} local files register.".format(len(self.__source_files)))

        if len(self.__source_files) == 0:
            Services.t_print("No files in {0}".format(source_folder))

    def get_data(self, byte_object, file_idx):
        """
        Get data from the file.
        """
        if isinstance(byte_object, bytearray):
            with open(self.__source_files[file_idx], 'rb') as t:
                byte_object += t.read()
        else:
            raise Exception("Function requires bytes array.")

    def get_next_file_id(self):
        if self.__index < len(self.__source_files):
            tmp = self.__index
            self.__index += 1
            return tmp
        return None

    def is_valid_file_id(self, object_id):
        if object_id < len(self.__source_files):
            return True

        return False

    @property
    def is_done(self):
        """
        Purpose: To check that do we still have some data to be stream.
        This function is only apply to finite data set. So, I not put it in the DataSource.
        :return: True or False
        """
        if self.__index < len(self.__source_files):
            return False

        return True


class LocalCachedDataSource(DataSource):
    """
    This class use data from local files as data source.
    -----------------------------------------------------------------------------------------
    CAUTION: The implementation of method in this class doesn't prevent from race condition.
    We implement this way because we rely on Thread in Python that is controlled by GIL.
    When, you change from Thread to Process Pool. You must implement some kind of lock to
    make the synchronization correct.
    -----------------------------------------------------------------------------------------
    """

    def __init__(self, source_folder='/', file_extension='*'):
        # Check that folder is exist or not, if not throw exception
        if not Services.is_folder_exist(source_folder):
            Services.t_print("{0} does not exist!".format(source_folder))

        if source_folder[-1] != '/':
            source_folder += '/'

        import time
        import glob
        self.__source_files = glob.glob(source_folder + '*.' + file_extension)
        self.__source_folder = source_folder
        self.__index = 0
        print("{0} local files register.".format(len(self.__source_files)))
        if len(self.__source_files) == 0:
            Services.t_print("No files in {0}".format(source_folder))

        # Start reading data into memory
        time1 = time.time()
        self.__data = list()
        for i, file in enumerate(self.__source_files):
            b = bytearray()
            self.__get_data(b, i)
            self.__data.append(b)
        time2 = time.time()

        print("Load all {0} files complete in {1} seconds.".format(len(self.__source_files), time2 - time1))

    def __get_data(self, byte_object, file_idx):
        """
        Get data from the file.
        """
        if isinstance(byte_object, bytearray):
            with open(self.__source_files[file_idx], 'rb') as t:
                byte_object += t.read()
        else:
            raise Exception("Function requires bytes array.")

    def get_data(self, byte_object, file_index):
        byte_object += self.__data[file_index]

    def get_next_file_id(self):
        if self.__index < len(self.__source_files):
            tmp = self.__index
            self.__index += 1
            return tmp
        return None

    def is_valid_file_id(self, object_id):
        if object_id < len(self.__source_files):
            return True

        return False

    @property
    def is_done(self):
        """
        Purpose: To check that do we still have some data to be stream.
        This function is only apply to finite data set. So, I not put it in the DataSource.
        :return: True or False
        """
        if self.__index < len(self.__source_files):
            return False

        return True


class TupleRates(object):
    """
    This function create a tuple rate simulation by reading a tuple creation pattern from file.
    The file must be in a list format and the number in the list refer to tuple creation rate in each second.
    """
    def __init__(self, tuple_rate_file):
        if Services.is_folder_exist(tuple_rate_file):
            Services.t_print("{0} does not exist!".format(tuple_rate_file))

        with open(tuple_rate_file) as t:
            self.__tuple_rate = eval(t.read())
            self.__cur_rate = 0

        self.__next_frame()

    def __next_frame(self):
        if len(self.__tuple_rate) > 0:
            self.__cur_rate = self.__tuple_rate.pop(0)
        else:
            Services.t_print("No tuple rate in the next frame")

    def get_delay(self):
        if self.__cur_rate == 0:
            self.__next_frame()
            return 1
        else:
            self.__cur_rate -= 1
            if self.__cur_rate == 0:
                self.__next_frame()
            return 0
