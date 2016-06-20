import datetime


class Setting(object):
    # REST Setting
    __node_name = None
    __node_addr = None
    __node_port = None
    __token = "None"

    # Mongodb Setting
    __mg_connection_string = None
    __db_name = None
    __table_feature_name = None
    __table_tree_name = None
    __table_meta_name = None
    __lc_storage = None

    @staticmethod
    def set_node_addr(addr=None):
        if addr:
            Setting.__node_addr = addr
        else:
            import socket
            from general.services import Services
            Setting.__node_addr = socket.gethostname()

            # if addr is valid
            if Services.is_valid_ipv4(Setting.__node_addr) or Services.is_valid_ipv6(Setting.__node_addr):
                return None

            # if addr is not valid
            Setting.__node_addr = Services.get_host_name_i()
            if Services.is_valid_ipv4(Setting.__node_addr) or Services.is_valid_ipv6(Setting.__node_addr):
                return None

            Services.t_print("Cannot get node ip address!")

    @staticmethod
    def read_cfg_from_file():
        from general.services import Services
        if not Services.is_file_exist('data_repository/configuration.json'):
            Services.t_print('data_repository/configuration.json does not exist')
        else:
            with open('data_repository/configuration.json', 'rt') as t:
                import json
                cfg = json.loads(t.read())

                from general.definition import Definition
                if  Definition.get_str_node_name() in cfg and \
                    Definition.get_str_node_port() in cfg and \
                    Definition.get_str_mongodb_setting() in cfg:

                    if not isinstance(cfg[Definition.get_str_node_port()], int):
                        Services.t_print("Node port must be number!")

                    Setting.__node_name = cfg[Definition.get_str_node_name()].strip()
                    Setting.__node_port = cfg[Definition.get_str_node_port()]
                    Setting.set_node_addr()

                    # Check for the internal structure of database setting
                    db_setting = cfg[Definition.get_str_mongodb_setting()]
                    if  Definition.MongoDB.get_str_connection_string() in db_setting and \
                        Definition.MongoDB.get_str_db_name() in db_setting and \
                        Definition.MongoDB.get_str_db_feature() in db_setting and \
                        Definition.MongoDB.get_str_db_tree() in db_setting and \
                        Definition.MongoDB.get_str_db_meta() in db_setting and \
                        Definition.MongoDB.get_str_lc_storage() in db_setting:

                        # Setting mongodb table
                        Setting.__mg_connection_string = db_setting[Definition.MongoDB.get_str_connection_string()].strip()
                        Setting.__db_name = db_setting[Definition.MongoDB.get_str_db_name()].strip()
                        Setting.__table_feature_name = db_setting[Definition.MongoDB.get_str_db_feature()].strip()
                        Setting.__table_tree_name = db_setting[Definition.MongoDB.get_str_db_tree()].strip()
                        Setting.__table_meta_name = db_setting[Definition.MongoDB.get_str_db_meta()].strip()
                        Setting.__lc_storage = db_setting[Definition.MongoDB.get_str_lc_storage()].strip()



                try:
                    pass
                except:
                    Services.t_print("Invalid data in configuration file.")

    @staticmethod
    def get_node_name():
        return Setting.__node_name

    @staticmethod
    def get_node_addr():
        return Setting.__node_addr

    @staticmethod
    def get_node_port():
        return Setting.__node_port

    @staticmethod
    def get_db_connection_string():
        return Setting.__mg_connection_string

    @staticmethod
    def get_token():
        return Setting.__token

    # Database region
    @staticmethod
    def get_str_database_name():
        return Setting.__db_name

    @staticmethod
    def get_str_table_feature():
        return Setting.__table_feature_name

    @staticmethod
    def get_str_table_meta_name():
        return Setting.__table_meta_name

    @staticmethod
    def get_str_table_linkage_matrix():
        return Setting.__table_tree_name

    @staticmethod
    def get_local_storage():
        return Setting.__lc_storage

"""

class Definitions(object):

    class Services(object):

        @staticmethod
        def get_string_service_path():
            return 'services'

        @staticmethod
        def get_string_command():
            return 'command'

        @staticmethod
        def get_string_client():
            return 'client'

        @staticmethod
        def get_string_client_alias():
            return 'alias'

        @staticmethod
        def get_string_client_addr():
            return 'addr'

    class Rest(object):

        @staticmethod
        def get_string_service_path():
            return 'dataRepository'

        @staticmethod
        def get_string_dump_features():
            return 'get_features'

        @staticmethod
        def get_string_count_features():
            return 'count'

        @staticmethod
        def get_string_req_command():
            return 'command'

        @staticmethod
        def get_string_request_token():
            return 'token'

        @staticmethod
        def get_string_id():
            return 'id'

        @staticmethod
        def get_string_realization():
            return 'realizations'

        @staticmethod
        def get_string_label():
            return 'label'

        @staticmethod
        def get_string_maker():
            return 'created_by'

    class DataLabels(object):

        @staticmethod
        def get_string_service_path():
            return 'dataLabels'

        @staticmethod
        def get_string_command():
            return 'command'

        @staticmethod
        def get_string_command_linkakge_m():
            return 'linkage_matrix'

        @staticmethod
        def get_string_command_tree():
            return 'labeled_tree'

        @staticmethod
        def get_string_command_row_idx():
            return 'row_index'

        @staticmethod
        def get_string_command_dump_meta():
            return 'meta_all'

    class Feature(object):

        @staticmethod
        def get_feature_name(_id):
            return str(_id) + '.p.zip'

        @staticmethod
        def get_string_feature():
            return 'features'

        @staticmethod
        def get_string_parameter():
            return 'parameters'

        @staticmethod
        def get_string_mapper_time():
            return 'time for mapper (s)'

    class MongoDB(object):

        class Features(object):
            @staticmethod
            def get_string_id():
                return 'id'

            @staticmethod
            def get_string_previous_id():
                return '_id'

            @staticmethod
            def get_string_feature_path():
                return 'feature_path'

            @staticmethod
            def get_string_realization_path():
                return 'realization_path'

            @staticmethod
            def get_string_created_by():
                return 'created_by'

            @staticmethod
            def get_string_created_date():
                return 'created_date'

            @staticmethod
            def get_string_is_labeled():
                return 'is_labeled'

            @staticmethod
            def get_string_is_enabled():
                return 'is_enabled'

            @staticmethod
            def get_dict_record(_id, prev_id, feature_path, realization_path, created_by, is_labeled):
                return {
                    Definitions.MongoDB.Features.get_string_id(): _id,
                    Definitions.MongoDB.Features.get_string_previous_id(): prev_id,
                    Definitions.MongoDB.Features.get_string_feature_path(): feature_path,
                    Definitions.MongoDB.Features.get_string_realization_path(): realization_path,
                    Definitions.MongoDB.Features.get_string_created_by(): created_by,
                    Definitions.MongoDB.Features.get_string_created_date(): datetime.datetime.now(),
                    Definitions.MongoDB.Features.get_string_is_labeled(): is_labeled,
                    Definitions.MongoDB.Features.get_string_is_enabled(): True
                }

        class LinkageMatrix(object):

            @staticmethod
            def get_string_left_child():
                return 'left_child'

            @staticmethod
            def get_string_right_child():
                return 'right_child'

            @staticmethod
            def get_string_proximity():
                return 'proximity'

            @staticmethod
            def get_string_num_of_nodes():
                return 'members_num'

        class Meta(object):
            @staticmethod
            def get_string_name():
                return 'name'

            @staticmethod
            def get_string_value():
                return 'value'

            @staticmethod
            def get_string_last_update():
                return 'last_update'
"""