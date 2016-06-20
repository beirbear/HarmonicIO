import falcon
import subprocess
from .configuration import Setting
from general.definition import Definition
from .pe_channels import PEChannels
from .messaging_system import MessagingServices, MessagesQueue


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


class MessageStreaming(object):
    def __init__(self):
        pass

    def on_get(self, req, res):
        """
        GET: /streamRequest?token=None
        This function is mainly respond with the available channel for streaming from data source.
        """
        if not Definition.get_str_token() in req.params:
            res.body = "Token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return

        # Check for the available channel
        channel = PEChannels.get_available_channel()
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

    def on_post(self, req, res):
        """
        POST: /streamRequest?token=None
        This function respond with getting a stream from data source or from messaging system.
        """
        if not Definition.get_str_token() in req.params:
            res.body = "Token is required."
            res.content_type = "String"
            res.status = falcon.HTTP_401
            return

        # Check that the PE is existing or not, if not insert and respond
        if Definition.REST.Batch.get_str_batch_addr() in req.params and \
           Definition.REST.Batch.get_str_batch_port() in req.params and \
           Definition.REST.Batch.get_str_batch_status() in req.params:

            # Check for data type
            if req.params[Definition.REST.Batch.get_str_batch_port()].isdigit() and \
               req.params[Definition.REST.Batch.get_str_batch_status()].isdigit():

                batch_port = int(req.params[Definition.REST.Batch.get_str_batch_port()])
                batch_status = int(req.params[Definition.REST.Batch.get_str_batch_status()])

                # Register channel
                PEChannels.register_channel(req.params[Definition.REST.Batch.get_str_batch_addr()],
                                            batch_port, batch_status)
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


class RESTService(object):
    def __init__(self):
        # Initialize REST Services
        from wsgiref.simple_server import make_server
        api = falcon.API()

        # Add route for getting status update
        api.add_route('/' + Definition.REST.get_str_status(), RequestStatus())

        # Add route for stream request
        api.add_route('/' + Definition.REST.get_str_stream_req(), MessageStreaming())

        # Establishing a REST server
        self.__server = make_server(Setting.get_node_addr(), Setting.get_node_port(), api)

    def run(self):
        print("REST Ready.....\n\n")
        self.__server.serve_forever()
