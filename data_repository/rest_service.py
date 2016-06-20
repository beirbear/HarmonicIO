import falcon
import subprocess
from general.dr_definition import Definition as df
from general.definition import Definition
from .configuration import Setting


class RequestStatus(object):
    def __init__(self):
        pass

    def get_machine_status(self):
        """
        Get machine status by calling a unix command and fetch for load average
        """
        res = str(subprocess.check_output(Definition.get_cpu_load_command())).strip()
        res = res.replace(",", "").replace("\\n", "").replace("'", "")
        *_, load1, load5, load15 = res.split(" ")
        return load1, load5, load15

    def on_get(self, req, res):
        """
        GET: /status?token={None}
        """
        if not Definition.get_str_token() in req.params:
            res.body = "Token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return

        if req.params[Definition.get_str_token()] == Setting.get_token():
            result = self.get_machine_status()
            res.body = '{ "' + Definition.get_str_node_name() + '": "' + Setting.get_node_name() + '", \
                         "' + Definition.get_str_node_addr() + '": "' + Setting.get_node_addr() + '", \
                         "' + Definition.get_str_load1() + '": ' + result[0] + ', \
                         "' + Definition.get_str_load5() + '": ' + result[1] + ', \
                         "' + Definition.get_str_load15() + '": ' + result[2] + ' }'
            res.content_type = "String"
            res.status = falcon.HTTP_200
        else:
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401


class DataObject(object):
    """
    REST Path: /dataRepository?
    This is a REST object component.
    This class dealing with only request about feature relation and file linkage.
    """

    def __init__(self, meta_storage):
        """
        :param meta_storage: Storage for pymongo
        """
        self.__meta_storage = meta_storage

    def on_get(self, req, res):
        """
        Purpose: Get data from the database
        GET: /dataRepository?token={None}
        GET: /dataRepository?token={None}&command={count}
        GET: /dataRepository?token={None}&command={get_features}
        """

        # Check for the presence of token attribute
        if Definition.get_str_token() not in req.params:
            """Token is required"""
            res.body = "Token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return None

        # Check for the value of token
        token_value = req.params[Definition.get_str_token()].strip()
        if token_value == Setting.get_token():
            """If the token is valid"""

            if df.Rest.get_string_req_command() in req.params:
                """If the request contain command option """
                if req.params[df.Rest.get_string_req_command()] == df.Rest.get_string_count_features():
                    """
                    GET: /dataRepository?token={None}&command={count}
                    Meaning: Count total record in the table
                    """
                    res.body = "Total records:" + str(self.__meta_storage.count_total_features())
                    res.content_type = "String"
                    res.status = falcon.HTTP_200

                elif req.params[df.Rest.get_string_req_command()] == df.Rest.get_string_dump_features():
                    """
                    GET: /dataRepository?token={None}&command={get_features}
                    Meaning: Get all features from the database. The content will be form in an tar format.
                    """
                    res.data = self.__meta_storage.get_all_features().getvalue()
                    res.content_type = "Byte"
                    res.status = falcon.HTTP_200
                else:
                    res.body = "Unknown command"
                    res.content_type = "String"
                    res.status = falcon.HTTP_401
            else:
                """
                GET: /dataRepository?token={None}
                Meaning: Select all from the table, because no parameter is specified
                """
                res.body = str(self.__meta_storage.dump_feature_table())
                res.content_type = "String"
                res.status = falcon.HTTP_200
        else:
            """
            Invalid Token
            """
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401

    def on_post(self, req, res):
        """
        Insert the data into database
        POST: /dataRepository?token={None}&id={data_id}&realization={path}
                                          &label={Undefined}&created_by={maker}
              Body = {Content}
        """
        # Check for token attribute
        if df.Rest.get_string_request_token() not in req.params:
            """Token is required"""
            res.body = "Token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return None

        # Check for required parameters
        if df.Rest.get_string_id() not in req.params or \
           df.Rest.get_string_realization() not in req.params or \
           df.Rest.get_string_label() not in req.params or \
           df.Rest.get_string_maker() not in req.params:
            """All required parameters is not presence"""
            res.body = "All requires attributes are not present"
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return None

        # Preparing the attributes
        token = req.params[df.Rest.get_string_request_token()].strip()
        current_id = req.params[df.Rest.get_string_id()].strip()

        """------------ NEED TO MODIFY TO SUPPORT ACTUAL PREV_ID ------------"""
        prev_id = 'dummy.com/sample_' + current_id
        """------------ NEED TO MODIFY TO SUPPORT ACTUAL PREV_ID ------------"""

        realization_path = req.params[df.Rest.get_string_realization()].strip()
        label = req.params[df.Rest.get_string_label()].strip()
        maker = req.params[df.Rest.get_string_maker()].strip()

        if token != Setting.get_token():
            """Check for token is it valid or not"""
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return None

        if not len(realization_path) and not len(current_id) and not len(label) and not len(maker):
            """Check if the parameter is supplied, but just an empty string"""
            res.body = "Incomplete data for some required parameters."
            res.content_type = "String"
            res.status = falcon.HTTP_400

        else:
            """All attributes are okay"""
            content = req.stream.read()
            if len(content) == 0:
                """ There is no content in the push request.
                    Respond with error.
                """
                res.body = "No content present in the body"
                res.content_type = "String"
                res.status = falcon.HTTP_401
                return None

            try:
                """Force push writing content into the local_storage"""
                f_path = df.Feature.get_feature_name(current_id)
                with open(Setting.get_local_storage() + f_path, 'wb') as w:
                    w.write(content)
            except Exception as e:
                print("Writing content into local storage error.\n" + str(e))
                res.body = "Writing content into data repository error!"
                res.content_type = "String"
                res.status = falcon.HTTP_401
                return None

            # Insert into the database
            if self.__meta_storage.insert_feature(current_id,
                                                  prev_id,
                                                  f_path,
                                                  realization_path,
                                                  maker,
                                                  label):
                res.body = "Insert feature complete."
                res.content_type = "String"
                res.status = falcon.HTTP_200

            else:
                res.body = "Insert feature error."
                res.content_type = "String"
                res.status = falcon.HTTP_429

    def on_put(self, req, res):
        """Request for update information in the database"""
        # raise Exception("Have not implemented yet!")
        res.body = "No service available for this request."
        res.content_type = "String"
        res.status = falcon.HTTP_400

    def on_delete(self, req, res):
        """
        Purpose: Purge the database (Only the feature linkage table)
        DELETE: /dataRepository?token={None}
        """
        if df.Rest.get_string_request_token() not in req.params:
            """Token is required"""
            res.body = "Token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return None

        # Preparing the token
        token = req.params[df.Rest.get_string_request_token()].strip()
        if token != Setting.get_token():
            """Invalid token"""
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401
        else:
            """Valid token. then, truncate the table."""
            self.__meta_storage.drop_feature_table()
            res.body = "Table has been dropped."
            res.content_type = "String"
            res.status = falcon.HTTP_200


class LabelObject(object):
    """
    REST Path: /dataLabels?
    This class is a REST object component.
    This class dealing with information about label. It involves with two tables in the database.
    """
    def __init__(self, meta_storage):
        """
        :param meta_storage: storage for mongodb
        """
        self.__meta_storage = meta_storage

    def on_get(self, req, res):
        """
        Purpose: get information about linkage matrix, row index and label name.
        GET: /dataLabels?command={distance_matrix|labeled_tree|row_index}&token={None}
        """

        # Check for the presence of the token attribute
        if df.Rest.get_string_request_token() not in req.params:
            res.body = "token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return None

        # Preparing the token
        token_value = req.params[df.Rest.get_string_request_token()].strip()
        if token_value == Setting.get_token():
            """If the token is valid"""

            """Check the command attribute"""
            if df.DataLabels.get_string_command() in req.params:
                """The command attribute is presence"""

                command = req.params[df.DataLabels.get_string_command()].strip()
                if df.DataLabels.get_string_command_linkakge_m() == command:
                    """GET: /dataLabels?command={linkage_matrix}&token={None}"""
                    # Get distance matrix
                    res.body = str(self.__meta_storage.dump_linkage_matrix())

                    res.content_type = "String"
                    res.status = falcon.HTTP_200

                elif df.DataLabels.get_string_command_tree() == command:
                    """GET: /dataLabels?command={labeled_tree}&token={None}"""
                    # Get tree structure
                    res.body = str(self.__meta_storage.get_value_from_meta_table(
                               df.DataLabels.get_string_command_tree()))
                    res.content_type = "String"
                    res.status = falcon.HTTP_200

                elif df.DataLabels.get_string_command_row_idx() == command:
                    """GET: /dataLabels?command={row_index}&token={None}"""
                    # Get row index
                    res.body = str(self.__meta_storage.get_value_from_meta_table(
                               df.DataLabels.get_string_command_row_idx()))
                    res.content_type = "String"
                    res.status = falcon.HTTP_200

                elif df.DataLabels.get_string_command_dump_meta() == command:
                    """GET: /dataLabels?command={meta_all}&token={None}"""
                    # Get row index
                    res.body = str(self.__meta_storage.dump_meta_table())
                    res.content_type = "String"
                    res.status = falcon.HTTP_200

                else:
                    res.body = "Invalid command"
                    res.content_type = "String"
                    res.status = falcon.HTTP_400

            else:
                res.body = "No command specified"
                res.content_type = "String"
                res.status = falcon.HTTP_400

        else:
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401

    def on_post(self, req, res):
        """
        Purpose: set the data about the labeling part into the database
        POST: /dataLabels?command={distance_matrix|labeled_tree|row_index}&token={None}
        """
        if df.Rest.get_string_request_token() not in req.params:
            res.body = "token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return None

        # Preparing the token value
        token_value = req.params[df.Rest.get_string_request_token()].strip()
        if token_value == Setting.get_token():
            """Token is present"""

            # Check for the command
            if df.DataLabels.get_string_command() not in req.params:
                res.body = "No command specified"
                res.content_type = "String"
                res.status = falcon.HTTP_400
                return None

            # Prepare the command
            command = req.params[df.DataLabels.get_string_command()].strip()
            content = req.stream.read()

            # Check the content
            if len(content) == 0:
                """ There is no content in the push request.
                    Respond with error.
                """
                res.body = "No content present in the body"
                res.content_type = "String"
                res.status = falcon.HTTP_401
                return None

            is_okay = True
            if df.DataLabels.get_string_command_linkakge_m() == command:
                """Insert the linkage matrix into the database"""
                if not self.__meta_storage.set_linkage_matrix(eval(content)):
                    is_okay = False
            elif df.DataLabels.get_string_command_tree() == command:
                """Insert the tree structure into the database"""
                if not self.__meta_storage.set_labeled_tree(content):
                    is_okay = False
            elif df.DataLabels.get_string_command_row_idx() == command:
                """Insert the row index into the database"""
                if not self.__meta_storage.set_row_index(content):
                    is_okay = False
            else:
                res.body = "Invalid requested command."
                res.content_type = "String"
                res.status = falcon.HTTP_400

            if not is_okay:
                res.body = "Insert data error."
                res.content_type = "String"
                res.status = falcon.HTTP_400
            else:
                res.body = "Insert or Update completed."
                res.content_type = "String"
                res.status = falcon.HTTP_200
        else:
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401


class RESTService(object):
    """
    Main class for the rest service
    """
    def __init__(self):
        from wsgiref.simple_server import make_server
        from .meta_storage import MetaStorage

        # Initialize MetaStorage
        meta_storage = MetaStorage()

        # Initialize Rest Service
        api = falcon.API()

        # Add route for getting status update
        api.add_route('/' + Definition.REST.get_str_status(), RequestStatus())
        api.add_route('/' + df.Rest.get_string_service_path(), DataObject(meta_storage))
        api.add_route('/' + df.DataLabels.get_string_service_path(), LabelObject(meta_storage))

        # Bind the service into the system
        self.__server = make_server(Setting.get_node_addr(), Setting.get_node_port(), api)

    def run(self):
        """
        Call this function to run the data repository service.
        """
        print("REST Ready.....\n\n")
        self.__server.serve_forever()
