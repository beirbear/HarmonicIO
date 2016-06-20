from pymongo import MongoClient
from .configuration import Setting
from general.definition import Definition as Definitions
import io
import tarfile
import datetime


class MetaStorage(object):
    """
    This class encapsulate the connection between application and mongodb.
    Just call this class for mongodb communication.
    It should be singleton, but there might be a case for multiple data connection,
    such as to multiple remote data source. So, I just keep it this way for now
    because I am still not sure about the further change. We might need to interface.
    """

    def __init__(self):
        # Create a mongodb client and test the connection
        try:
            self.__client = MongoClient(Setting.get_db_connection_string())
            self.__db = self.__client[Setting.get_str_database_name()]
        except Exception as e:
            print("""\Create database connection error.
                     \Please make sure the mongodb server is running""" + '\n' + str(e))
            exit(-1)

    def insert_feature(self, _id, prev_id, f_path, r_path, created_by, is_labeled):
        """
        Purpose: insert the feature and its link to the database.
        :param _id: the id of the feature. It must be number and generate from server side.
        :param prev_id: the full link that we can trace back to the stream request.
        :param f_path: feature path (link to the local storage of the file in data repository).
        :param r_path: realization path that stores in the HDFS or swift.
        :param created_by: the num of the process which initiate the stream.
        :param is_labeled: status that indicate that does this feature has been clustered.
        :return: Success or Fail
        """
        res = self.__db[Setting.get_str_table_feature()].insert_one(
              Definitions.MongoDB.Features.get_dict_record(_id, prev_id, f_path, r_path, created_by, is_labeled))

        if res.inserted_id:
            return True

        return False

    def count_total_features(self):
        """
        Purpose: count the total record
        :return: number of total features
        """
        return self.__db[Setting.get_str_table_feature()].count()

    def close_connection(self):
        self.__client.close()

    def get_all_features(self):
        """
        Purpose: dump all features file into tarball for processing in the knowledge discovery node.
        :return:
        """

        # In-memory tarball
        tar_byte = io.BytesIO()
        cursor = self.__db[Setting.get_str_table_feature()].find()
        out = tarfile.open(fileobj=tar_byte, mode='w')

        # Tarball every file at the moment
        for item in cursor:
            out.add(Setting.get_local_storage() + item[Definitions.MongoDB.Features.get_string_feature_path()])
        out.close()

        return tar_byte

    def dump_feature_table(self):
        """
        Purpose: dump every records to see the content inside the feature table.
        :return: records in the feature table.
        """
        if Setting.get_str_table_feature() not in self.__db.collection_names():
            return "Table has not been created yet."

        cursor = self.__db[Setting.get_str_table_feature()].find()
        return [item for item in cursor]

    def drop_database(self):
        """
        Purpose: drop feature table
        """
        self.__db[Setting.get_str_database_name()].drop()

    def set_linkage_matrix(self, content):
        """
        Purpose: set feature table
        """

        """ Truncate the existing data """
        # Truncate the table first
        if Setting.get_str_table_linkage_matrix() in self.__db.collection_names():
            self.__db[Setting.get_str_table_linkage_matrix()].drop()

        # Insert records into linkage matrix
        for l_node, r_node, distance, clust_num in content:
            res = self.__db[Setting.get_str_table_linkage_matrix()].insert_one({
                    Definitions.MongoDB.LinkageMatrix.get_string_left_child(): l_node,
                    Definitions.MongoDB.LinkageMatrix.get_string_right_child(): r_node,
                    Definitions.MongoDB.LinkageMatrix.get_string_proximity(): distance,
                    Definitions.MongoDB.LinkageMatrix.get_string_num_of_nodes(): clust_num
                    })

        if res.inserted_id:
            return True

        return False

    def set_labeled_tree(self, content):
        """
        Purpose: insert or replace the content about tree label name
        :param content: tree name
        :return: Success or Fail
        """
        self.__db[Setting.get_str_table_meta_name()].remove({
            Definitions.MongoDB.Meta.get_string_name(): Definitions.DataLabels.get_string_command_tree()})

        res = self.__db[Setting.get_str_table_meta_name()].insert_one({
            Definitions.MongoDB.Meta.get_string_name(): Definitions.DataLabels.get_string_command_tree(),
            Definitions.MongoDB.Meta.get_string_value(): content,
            Definitions.MongoDB.Meta.get_string_last_update(): datetime.datetime.now()})

        if res.inserted_id:
            return True

        return False

    def set_row_index(self, content):
        """
        Purpose: insert or replace the content about row_index
        :param content: row_index
        :return: Success or Fail
        """
        self.__db[Setting.get_str_table_meta_name()].remove({
            Definitions.MongoDB.Meta.get_string_name(): Definitions.DataLabels.get_string_command_row_idx()})

        res = self.__db[Setting.get_str_table_meta_name()].insert_one({
            Definitions.MongoDB.Meta.get_string_name(): Definitions.DataLabels.get_string_command_row_idx(),
            Definitions.MongoDB.Meta.get_string_value(): content,
            Definitions.MongoDB.Meta.get_string_last_update(): datetime.datetime.now()})

        if res.inserted_id:
            return True

        return False

    def dump_linkage_matrix(self):
        """
        Purpose: dump the linkage matrix
        :return:
        """
        if Setting.get_str_table_linkage_matrix() not in self.__db.collection_names():
            return "Table has not been created yet."

        cursor = self.__db[Setting.get_str_table_linkage_matrix()].find()

        res = []
        for item in cursor:
            res.append([int(item[Definitions.MongoDB.LinkageMatrix.get_string_left_child()]),
                        int(item[Definitions.MongoDB.LinkageMatrix.get_string_right_child()]),
                        float(item[Definitions.MongoDB.LinkageMatrix.get_string_proximity()]),
                        int(item[Definitions.MongoDB.LinkageMatrix.get_string_num_of_nodes()])])

        return res

    def get_value_from_meta_table(self, value):
        """
        Purpose: query the data in meta table and return
        :param value: parameter name
        :return: query result
        """
        if Setting.get_str_table_meta_name() not in self.__db.collection_names():
            return "Table has not been created yet."

        cursor = self.__db[Setting.get_str_table_meta_name()].find({
            Definitions.MongoDB.Meta.get_string_name(): value})

        res = []
        for item in cursor:
            res.append(eval(item[Definitions.MongoDB.Meta.get_string_value()]))

        return res

    def dump_meta_table(self):
        """
        Purpose: get everything in the meta table
        :return: query result (String)
        """
        try:
            if Setting.get_str_table_meta_name() not in self.__db.collection_names():
                return "Table has not been created yet."

            cursor = self.__db[Setting.get_str_table_meta_name()].find()

            res = []
            for item in cursor:
                res += [item[Definitions.MongoDB.Meta.get_string_name()],
                        eval(item[Definitions.MongoDB.Meta.get_string_value()])]

            return res
        except Exception as e:
            print("Error, " + str(e))

    @property
    def total_keys(self):
        raise Exception("Have not implement exception")
