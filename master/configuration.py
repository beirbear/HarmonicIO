class Setting(object):
    __node_name = None
    __node_addr = None
    __node_port = None
    __node_data_port_start = None
    __node_data_port_stop = None
    __std_idle_time = None
    __token = "None"

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
    def get_node_name():
        return Setting.__node_name

    @staticmethod
    def get_node_addr():
        return Setting.__node_addr

    @staticmethod
    def get_node_port():
        return Setting.__node_port

    @staticmethod
    def get_data_port_start():
        return Setting.__node_data_port_start

    @staticmethod
    def get_data_port_stop():
        return Setting.__node_data_port_stop

    @staticmethod
    def get_std_idle_time():
        return Setting.__std_idle_time

    @staticmethod
    def get_token():
        return Setting.__token

    @staticmethod
    def read_cfg_from_file():
        from general.services import Services
        if not Services.is_file_exist('master/configuration.json'):
            Services.t_print('master/configuration.json does not exist')
        else:
            with open('master/configuration.json', 'rt') as t:
                import json
                cfg = json.loads(t.read())

                try:
                    from general.definition import Definition
                    # Check for the json structure
                    if  Definition.get_str_node_name() in cfg and \
                        Definition.get_str_node_port() in cfg and \
                        Definition.get_str_master_addr() in cfg and \
                        Definition.get_str_data_port_range() in cfg and \
                        Definition.get_str_idle_time() in cfg:
                        # Check port number is int or not
                        if not isinstance(cfg[Definition.get_str_node_port()], int):
                            Services.t_print("Node port must be integer")
                        elif not isinstance(cfg[Definition.get_str_data_port_range()], list):
                            Services.t_print("Port range must be list")
                        elif not (isinstance(cfg[Definition.get_str_data_port_range()][0], int) and \
                                  isinstance(cfg[Definition.get_str_data_port_range()][1], int)):
                            Services.t_print("Port range must be integer")
                        elif len(cfg[Definition.get_str_data_port_range()]) != 2:
                            Services.t_print("Port range must compost of two elements: start, stop")
                        elif not isinstance(cfg[Definition.get_str_idle_time()], int):
                            Services.t_print("Idle time must be integer")
                        elif cfg[Definition.get_str_data_port_range()][0] > \
                             cfg[Definition.get_str_data_port_range()][1]:
                            Services.t_print("Start port range must greater than stop port range")
                        else:
                            Setting.__node_name = cfg[Definition.get_str_node_name()].strip()
                            Setting.__node_port = cfg[Definition.get_str_node_port()]
                            Setting.__node_data_port_start = cfg[Definition.get_str_data_port_range()][0]
                            Setting.__node_data_port_stop = cfg[Definition.get_str_data_port_range()][1]
                            Setting.__std_idle_time = cfg[Definition.get_str_idle_time()]
                            print("Load setting successful")

                        if  Services.is_valid_ipv4(cfg[Definition.get_str_master_addr()]) or \
                            Services.is_valid_ipv6(cfg[Definition.get_str_master_addr()]):
                            Setting.set_node_addr(cfg[Definition.get_str_master_addr()])
                        else:
                            print("Assigning master ip address automatically.")
                            Setting.set_node_addr()

                    else:
                        Services.t_print("Invalid data in configuration file.")
                except:
                    Services.t_print("Invalid data in configuration file.")
