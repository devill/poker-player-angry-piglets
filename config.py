from pymongo import MongoClient
import ssl
import threading
import time

# import player

MONGO_JSON_URL = 'mongodb://web:almafa@aws-us-east-1-portal.22.dblayer.com:16806,aws-us-east-1-portal.23.dblayer.com:16806/admin?ssl=true'

config_instance = None


class Config(object):
    version = 'initial config'
    refresh_interval = 5

    def __init__(self):
        # self.log = player.log
        self._start_thread()

    @staticmethod
    def get_instance(*args, **kwargs):
        global config_instance

        if config_instance is None:
            config_instance = Config(*args, **kwargs)

        return config_instance

    def load(self):
        client = MongoClient(MONGO_JSON_URL,ssl_cert_reqs=ssl.CERT_NONE)

        config_json = client.config.config.find_one({})

        for k, v in config_json.iteritems():
            self.__setattr__(k, v)

    def _start_thread(self):
        thread = threading.Thread(target=self._load)
        thread.start()

    def _load(self):
        while True:
            self.load()
            time.sleep(self.refresh_interval)
