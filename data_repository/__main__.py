"""
Application entry point
"""


def run_rest_service():
    # This function is for running rest service
    from .rest_service import RESTService
    rest = RESTService()
    rest.run()


def main():
    # Update configuration from the local file
    from .configuration import Setting
    Setting.read_cfg_from_file()

    # Print instance information
    print("Node name: {0}\nNode address: {1}".format(Setting.get_node_name(), Setting.get_node_addr()))

    # Reset data in the database
    from .meta_storage import MetaStorage
    meta_storage = MetaStorage()
    meta_storage.drop_database()
    print("Clear data in the database complete.")

    # Reset data in the local storage
    from general.services import Services
    if not Services.is_folder_exist(Setting.get_local_storage()):
        Services.t_print(Setting.get_local_storage() + " does not exist! (Local Storage).")

    # Get file from the folder
    import glob
    import os
    files = glob.glob(Setting.get_local_storage() + "*")
    for file in files:
        os.remove(file)
    print("Clear {0} files in the local storage complete.".format(len(files)))

    # Create a thread for running REST service
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor()
    pool.submit(run_rest_service)

if __name__ == '__main__':
    # Call the main flow of the program
    main()
