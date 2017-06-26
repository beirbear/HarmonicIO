import queue
from general.services import Services
from general.definition import Definition


class DataStatStatus(object):
    PENDING = 0
    PROCESSING = 1
    RESTREAM = 2


class LookUpTable(object):

    class Workers(object):
        __workers = {}

        @staticmethod
        def add_worker(dict_input):
            dict_input[Definition.get_str_last_update()] = Services.get_current_timestamp()
            LookUpTable.Workers.__workers[dict_input[Definition.get_str_node_addr()]] = dict_input

        @staticmethod
        def del_worker(worker_addr):
            del LookUpTable.Workers.__workers[worker_addr]

    class Containers(object):
        __containers = {}

        @staticmethod
        def add_container(dict_input):
            pass

        @staticmethod
        def update_container(dict_input):
            """
            queue_fifo.py
            import queue

            q = queue.Queue()

            for i in range(5):
                q.put(i)

            while not q.empty():
                print(q.get(), end=' ')
            print()
            """

        @staticmethod
        def get_candidate_container(image_name):
            if not image_name in LookUpTable.Containers.__containers:
                return None

            return LookUpTable.Containers.__containers[image_name].get()

    @staticmethod
    def update_worker(dict_input):
        LookUpTable.Workers.add_worker(dict_input)

    @staticmethod
    def get_candidate_container(image_name):
        LookUpTable.Containers.get_candidate_container(image_name)
