import importlib

falcon_spec = importlib.util.find_spec("falcon")
if falcon_spec is None:
    raise Exception("Falcon module has not been installed.")

falcon_spec = importlib.util.find_spec("urllib3")
if falcon_spec is None:
    raise Exception("urllib3 module has not been installed.")
