"""
Master entry point
"""


def run_rest_service():
    """
    Run rest as in a thread function
    """
    from .rest_service import RESTService
    rest = RESTService()
    rest.run()

def run_msg_service():
    """
    Run msg service to eliminate back pressure
    """
    from .configuration import Setting
    from .server_socket import ThreadedTCPServer, ThreadedTCPRequestHandler
    import threading
    server = ThreadedTCPServer((Setting.get_node_addr(), Setting.get_data_port_start()),
                               ThreadedTCPRequestHandler, bind_and_activate=True)

    # Start a thread with the server -- that thread will then start one
    server_thread = threading.Thread(target=server.serve_forever)

    # Exit the server thread when the main thread terminates
    server_thread.daemon = True

    print("Enable Messaging System.")

    server_thread.start()

    """ Have to test for graceful termination. """
    # server.shutdown()
    # server.server_close()

if __name__ == '__main__':
    """
    Entry point
    """
    print("Running Harmonic Master")

    # Load configuration from file
    from .configuration import Setting
    Setting.read_cfg_from_file()

    # Print instance information
    print("Node name: {0}\nNode address: {1}".format(Setting.get_node_name(), Setting.get_node_addr()))
    print("Port range: {0} to {1} ({2} ports available) ".format(Setting.get_data_port_start(),
                                                                 Setting.get_data_port_stop(),
                                                                 Setting.get_data_port_stop() -
                                                                 Setting.get_data_port_start()))

    # Create thread for handling REST Service
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor()

    # Run messaging system service
    pool.submit(run_msg_service)

    # Binding commander to the rest service and enable REST service
    pool.submit(run_rest_service)

