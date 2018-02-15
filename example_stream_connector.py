from harmonicIO.stream_connector.stream_connector import StreamConnector

config = {'master_host': '192.168.0.84',
          'master_port': 8080,
          'container_name': 'benblamey/hio-example:latest',
          'container_os': 'ubuntu'}

# std_idle_time is in seconds
sc = StreamConnector(config['master_host'], config['master_port'], max_try=1, std_idle_time=1)

message_bytes = bytearray('test data', encoding='utf-8')

sc.send_data(config['container_name'],
             config['container_os'],
             message_bytes)
