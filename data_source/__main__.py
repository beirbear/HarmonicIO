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
    print("Node name : {0}\nNode address: {1}".format(Setting.get_node_name(), Setting.get_node_addr()))
    print("Server address : {0}\nServer port: {1}".format(Setting.get_server_addr(), Setting.get_server_port()))

    # Load tuples from local file
    from .data_source import LocalCachedDataSource
    data_source = LocalCachedDataSource(source_folder='/home/ubuntu/utility/data_source', file_extension='p')

    # Create thread for handling REST Service
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor()

    # Binding commander to the rest service and enable REST service
    pool.submit(run_rest_service)
