"""
DataSource application entry point.
"""


def run_rest_service():
    """
    Run rest as in a thread function
    """
    from .rest_service import RESTService
    rest = RESTService()
    rest.run()

if __name__ == '__main__':
    """
    Entry point
    """
    print("Running Harmonic DataSource")

    # Load Setting from file
    from .configuration import Setting
    Setting.read_cfg_from_file()

    # Print instance information
    print("Node name: {0}\nNode address: {1}".format(Setting.get_node_name(), Setting.get_node_addr()))
    print("Server address: {0}\nServer port: {1}".format(Setting.get_server_addr(), Setting.get_server_port()))

    # Load tuples from local file
    from .data_source import LocalCachedDataSource
    data_source = LocalCachedDataSource(source_folder='/home/beir_bear/data_source', file_extension='p')

    # Create thread for handling REST Service
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor()

    # Binding commander to the rest service and enable REST service
    pool.submit(run_rest_service)

    # Create a master connector
    from .stream_connector import StreamConnector
    stream_connector = StreamConnector()

    # Wait for the master to be active
    import time

    while not stream_connector.is_master_alive():
        time.sleep(Setting.get_std_idle_time())

    # Wait for status
    # while not Setting.is_running:
    #     time.sleep(Setting.get_std_idle_time())

    # Create data rate simulation
    from .data_source import TupleRates
    tuple_rate = TupleRates('data_source/tuple_rates/tuple_intermittent.txt')

    # Start streaming
    file_index = 0
    while not data_source.is_done:
        # Mechanism here
        # Send a message to a master
        data = bytearray()
        data_source.get_data(data, file_index)
        stream_connector.send_data(data)

        # Sample of delay in data creation time.
        time.sleep(tuple_rate.get_delay())
        exit()
