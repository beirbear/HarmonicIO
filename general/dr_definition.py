from datetime import datetime


class Definition(object):
    """
    This class is a definition for data repository.
    """
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
                    Definition.MongoDB.Features.get_string_id(): _id,
                    Definition.MongoDB.Features.get_string_previous_id(): prev_id,
                    Definition.MongoDB.Features.get_string_feature_path(): feature_path,
                    Definition.MongoDB.Features.get_string_realization_path(): realization_path,
                    Definition.MongoDB.Features.get_string_created_by(): created_by,
                    Definition.MongoDB.Features.get_string_created_date(): datetime.now(),
                    Definition.MongoDB.Features.get_string_is_labeled(): is_labeled,
                    Definition.MongoDB.Features.get_string_is_enabled(): True
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
