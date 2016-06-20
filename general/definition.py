class BatchErrorCode:
    SUCCESS = 0
    CREATE_SOCKET_ERROR = 1
    PROCESSING_ERROR = 2


class CStatus:
    AVAILABLE = 0
    BUSY = 1


class Definition(object):
    @staticmethod
    def get_str_node_name():
        return "node_name"

    @staticmethod
    def get_str_node_addr():
        return "node_addr"

    @staticmethod
    def get_str_node_port():
        return "node_port"

    @staticmethod
    def get_str_server_addr():
        return "server_addr"

    @staticmethod
    def get_str_server_port():
        return "server_port"

    @staticmethod
    def get_str_ext_process():
        return "ext_process"

    @staticmethod
    def get_str_master_addr():
        return "master_addr"

    @staticmethod
    def get_str_master_port():
        return "master_port"

    @staticmethod
    def get_str_repo_addr():
        return "repo_addr"

    @staticmethod
    def get_str_repo_port():
        return "repo_port"

    @staticmethod
    def get_str_idle_time():
        return "std_idle_time"

    @staticmethod
    def get_str_data_port_range():
        return "node_data_port_range"

    @staticmethod
    def get_str_idle_time():
        return "std_idle_time"

    @staticmethod
    def get_str_token():
        return "token"

    @staticmethod
    def get_str_load1():
        return "load1"

    @staticmethod
    def get_str_load5():
        return "load5"

    @staticmethod
    def get_str_load15():
        return "load15"

    @staticmethod
    def get_cpu_load_command():
        return ['uptime', '|', 'awk', '{ print $8 $9 $10}']

    class Server(object):
        @staticmethod
        def get_str_check_master(addr, port, token):
            return "http://" + addr + ":" + str(port) + "/" + Definition.REST.get_str_status() + "?" + \
                   Definition.REST.get_str_token() + "=" + token

        @staticmethod
        def get_str_push_req(addr, port, token):
            return "http://" + addr + ":" + str(port) + "/" + Definition.REST.get_str_stream_req() + "?" + \
                   Definition.REST.get_str_token() + "=" + token

    class REST(object):
        @staticmethod
        def get_str_status():
            return "status"

        @staticmethod
        def get_str_stream_req():
            return "streamRequest"

        @staticmethod
        def get_str_token():
            return "token"

        class Batch(object):
            @staticmethod
            def get_str_batch_addr():
                return "batch_addr"

            @staticmethod
            def get_str_batch_port():
                return "batch_port"

            @staticmethod
            def get_str_batch_status():
                return "batch_status"

    @staticmethod
    def get_channel_response(addr, port, t_id):
        return '{ "c_addr": "' + addr + '", "c_port": ' + str(port) + ', "t_id": ' + str(t_id) + '}'

    @staticmethod
    def get_str_mongodb_setting():
        return "mongodb_setting"

    class MongoDB(object):

        @staticmethod
        def get_str_connection_string():
            return "connection_string"

        @staticmethod
        def get_str_db_name():
            return "db_name"

        @staticmethod
        def get_str_db_feature():
            return "db_features"

        @staticmethod
        def get_str_db_tree():
            return "db_tree"

        @staticmethod
        def get_str_db_meta():
            return "db_meta"

        @staticmethod
        def get_str_lc_storage():
            return "lc_storage"
