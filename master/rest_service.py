import falcon
from .configuration import Setting
from general.definition import Definition, CStatus
from .pe_channels import PEChannels
from .messaging_system import MessagesQueue
from general.services import SysOut
from .meta_table import LookUpTable


class RequestStatus(object):

    def __init__(self):
        pass

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
            from general.services import Services
            from general.definition import CRole

            result = Services.get_machine_status(Setting, CRole.MASTER)

            res.body = str(result)
            res.content_type = "String"
            res.status = falcon.HTTP_200
        else:
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401

    def on_put(self, req, res):
        """
        PUT: /status?token={None}
        """
        if not Definition.get_str_token() in req.params:
            res.body = "Token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return

        if req.params[Definition.get_str_token()] == Setting.get_token():
            raw = str(req.stream.read(), 'UTF-8')
            data = eval(raw)

            LookUpTable.update_worker(data)
            SysOut.debug_string("Update worker status ({0})".format(data[Definition.get_str_node_name()]))

            res.body = "Okay"
            res.content_type = "String"
            res.status = falcon.HTTP_200
        else:
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401


class MessageStreaming(object):
    def __init__(self):
        pass

    def on_get(self, req, res):
        """
        return "&c_name=" + container_name + "&c_os=" + container_os + "&priority=" + str(priority)
        GET: /streamRequest?token=None
        This function is mainly respond with the available channel for streaming from data source.
        """

        if not Definition.get_str_token() in req.params:
            res.body = "Token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return

        # Check for required parameter.
        if not Definition.Container.get_str_container_name() in req.params:
            res.body = "Container name is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return

        if not Definition.Container.get_str_container_os() in req.params:
            res.body = "Container os is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return

        if not Definition.Container.get_str_data_source() in req.params:
            res.body = "Data digest is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return

        # parameters
        container_name = req.params[Definition.Container.get_str_container_name()].strip()
        container_os = req.params[Definition.Container.get_str_container_os()].strip()
        data_source = req.params[Definition.Container.get_str_data_source()].strip()
        digest = req.params[Definition.Container.get_str_data_digest()].strip()
        container_priority = 0

        if Definition.Container.get_str_container_priority() in req.params:
            from general.services import Services
            if Services.is_str_is_digit(req.params[Definition.Container.get_str_container_priority()]):
                container_priority = int(req.params[Definition.Container.get_str_container_priority()])
            else:
                res.body = "Container priority is not digit."
                res.content_type = "String"
                res.status = falcon.HTTP_401
                return

        # Check for the availability of the container
        ret = LookUpTable.get_candidate_container(container_name)

        if ret:
            # res.body = Definition.Master.get_str_end_point(ret[D])
            res.body = "just a moment"
            res.content_type = "String"
            res.status = falcon.HTTP_200
        else:
            # No streaming end-point available
            ret = Definition.Master.get_str_end_point_MS(Setting)
            res.body = str(ret)
            res.content_type = "String"
            res.status = falcon.HTTP_200


        """
        # Push info into request table.
        DataStat.add_data_stat(MessagingServices.get_new_msg_id(),
                               data_source,
                               container_name,
                               container_os,
                               container_priority,
                               digest)

        SysOut.debug_string(str(DataStat.get_stat_table()))
        


        # Check for the available channel
        channel = PEChannels.get_available_channel(group="optimize")
        if channel:
            # If channel is available
            res.body = Definition.get_channel_response(channel[0], channel[1], MessagingServices.get_new_msg_id())
            res.content_type = "String"
            res.status = falcon.HTTP_200
        else:
            if MessagesQueue.is_queue_available():
                # Channel is not available, respond with messaging system channel
                res.body = Definition.get_channel_response(Setting.get_node_addr(), Setting.get_data_port_start(),
                                                           MessagingServices.get_new_msg_id())
                res.content_type = "String"
                res.status = falcon.HTTP_200
            else:
                # Message in queue is full
                res.body = Definition.get_channel_response("0.0.0.0", 0, 0)
                res.content_type = "String"
                res.status = falcon.HTTP_406
                """

    def on_post(self, req, res):
        """
        POST: /streamRequest?token=None
        This function invoked by the driver in micro-batch in the container.
        It responds with getting a stream from data source or from messaging system.
        """
        if not Definition.get_str_token() in req.params:
            res.body = "Token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return

        # Check that the PE is existing or not, if not insert and respond
        if Definition.REST.Batch.get_str_batch_addr() in req.params and \
           Definition.REST.Batch.get_str_batch_port() in req.params and \
           Definition.REST.Batch.get_str_batch_status() in req.params and \
           Definition.Container.get_str_container_name() in req.params:

            # Check for data type
            if req.params[Definition.REST.Batch.get_str_batch_port()].isdigit() and \
               req.params[Definition.REST.Batch.get_str_batch_status()].isdigit():

                batch_port = int(req.params[Definition.REST.Batch.get_str_batch_port()])
                batch_status = int(req.params[Definition.REST.Batch.get_str_batch_status()])
                image_name = req.params[Definition.Container.get_str_container_name()].strip()

                # If queue contain data, ignore update and stream from queue
                length = MessagesQueue.get_queues_length(image_name)
                SysOut.warn_string("image_name: " + image_name)
                SysOut.warn_string("length: " + str(length))
                SysOut.warn_string("batch_status: " + str(batch_status))
                SysOut.warn_string("CStatus: " + str(CStatus.AVAILABLE))

                if not length:
                    """
                    1.) No item in queue.
                    2.) Flag the container status to available in the LookUpTable
                    """
                    SysOut.debug_string("No item in queue!")
                    res.body = "No item in queue"
                    res.content_type = "String"
                    res.status = falcon.HTTP_200
                    return

                """
                1.) Item in queue
                2.) Get item for specific container
                3.) Respond with content from the LookUpTable, and do not remain flag the container to busy.
                """

                if length > 0 and batch_status == CStatus.AVAILABLE:
                    res.data = bytes(MessagesQueue.pop_queue(image_name))
                    res.content_type = "Bytes"
                    res.status = falcon.HTTP_203
                else:
                    # Register channel
                    # PEChannels.register_channel(req.params[Definition.REST.Batch.get_str_batch_addr()],
                    #                             batch_port, batch_status)
                    res.body = "OK"
                    res.content_type = "String"
                    res.status = falcon.HTTP_200

            else:
                res.body = "Invalid data type!"
                res.content_type = "String"
                res.status = falcon.HTTP_406
        else:
            res.body = "Invalid parameters!"
            res.content_type = "String"
            res.status = falcon.HTTP_406


class MessagesQuery(object):
    def __init__(self):
        pass

    def on_get(self, req, res):
        """
        GET: /messagesQuery?token=None&command=queueLength
         This function inquiry about the number of messages in queue. For dealing with create a new instance.
        """
        if not Definition.get_str_token() in req.params:
            res.body = "Token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return

        if not Definition.MessagesQueue.get_str_command() in req.params:
            res.body = "No command specified."
            res.content_type = "String"
            res.status = falcon.HTTP_406
            return

        if req.params[Definition.MessagesQueue.get_str_command()] == Definition.MessagesQueue.get_str_queue_length():
            res.body = str(MessagesQueue.get_queues_all())
            res.content_type = "String"
            res.status = falcon.HTTP_200
            return

        if req.params[Definition.MessagesQueue.get_str_command()] == Definition.MessagesQueue.get_str_current_id():
            res.body = "None"
            res.content_type = "String"
            res.status = falcon.HTTP_200
            return


class RESTService(object):
    def __init__(self):
        # Initialize REST Services
        from wsgiref.simple_server import make_server
        api = falcon.API()

        # Add route for getting status update
        api.add_route('/' + Definition.REST.get_str_status(), RequestStatus())

        # Add route for stream request
        api.add_route('/' + Definition.REST.get_str_stream_req(), MessageStreaming())

        # Add route for msg query
        api.add_route('/' + Definition.REST.get_str_msg_query(), MessagesQuery())

        # Establishing a REST server
        self.__server = make_server(Setting.get_node_addr(), Setting.get_node_port(), api)

    def run(self):
        SysOut.out_string("REST Ready.....")

        self.__server.serve_forever()
