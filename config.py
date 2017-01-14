import json
import urllib
import threading
import time

import player


CONFIG_JSON_URL = 'https://raw.githubusercontent.com/knifeofdreams/jsonconfig/master/config.json'


class Config(object):
    version = 'config not loaded'
    refresh_interval = 5

    def __init__(self):
        self._start_thread()
        self.log = player.log

    def load(self):
        try:
            r = urllib.urlopen(CONFIG_JSON_URL)
            config_json = json.load(r)

            for k, v in config_json.iteritems():
                self.__setattr__(k, v)
                self.log.info('config values %s = %s', k, v)

            self.log.info('finished loading config file')
        except Exception as e:
            self.log.error('config exception caught: %s', e)

    def _start_thread(self):
        thread = threading.Thread(target=self._load)
        thread.start()

    def _load(self):
        while True:
            self.load()
            time.sleep(self.refresh_interval)