import importlib

falcon_spec = importlib.util.find_spec("falcon")
if falcon_spec is None:
    raise Exception("Falcon module has not been installed.")

pymongo_spec = importlib.util.find_spec("pymongo")
if pymongo_spec is None:
    raise Exception("pymongo module has not been installed.")
