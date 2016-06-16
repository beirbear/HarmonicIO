class MessagingConfiguration(object):
    __queue_threshold = 4
    __max_in_memory_msg = 500

    @staticmethod
    def get_queue_threshold():
        return MessagingConfiguration.__queue_threshold

    @staticmethod
    def get_max_in_memory_msg():
        return  MessagingConfiguration.__max_in_memory_msg


class MessagesQueue(object):
    __msg_queue = []

    @staticmethod
    def push_to_queue(item):
        if not isinstance(item, bytearray):
            raise Exception("Invalid implementation! requires byte array but got something else.")

        MessagesQueue.__msg_queue.append([item])
        MessagesQueue.__check_for_scale()

    @staticmethod
    def get_queue_length():
        return len(MessagesQueue.__msg_queue)

    @staticmethod
    def pop_queue(index):
        return MessagesQueue.__msg_queue.pop(index)

    @staticmethod
    def is_queue_available():
        if MessagesQueue.get_queue_length() < MessagingConfiguration.get_max_in_memory_msg():
            return True

        return False

    @staticmethod
    def __check_for_scale():
        print("There are {0} tuples in queues. Need more PE now!".format(MessagesQueue.get_queue_length()))


class MessagingServices(object):
    __msg_id = 0

    @staticmethod
    def get_new_msg_id():
        MessagingServices.__msg_id += 1
        return MessagingServices.__msg_id