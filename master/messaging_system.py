class MessagesQueue(object):
    __msg_queue = []

    @staticmethod
    def push_to_queue(item):
        if not isinstance(item, bytearray):
            raise Exception("Invalid implementation! requires byte array but got something else.")

        MessagesQueue.__msg_queue.append([item])

    @staticmethod
    def get_queue_length():
        return len(MessagesQueue.__msg_queue)

    @staticmethod
    def pop_queue(index):
        return MessagesQueue.__msg_queue.pop(index)


class MessagingServices(object):
    __msg_id = 0

    @staticmethod
    def get_new_msg_id():
        MessagingServices.__msg_id += 1
        return MessagingServices.__msg_id