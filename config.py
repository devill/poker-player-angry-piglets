from pymongo import MongoClient
import ssl
import threading
import time

import player

MONGO_JSON_URL = 'mongodb://web:almafa@aws-us-east-1-portal.22.dblayer.com:16806,aws-us-east-1-portal.23.dblayer.com:16806/admin?ssl=true'

config_instance = None


class Config(object):
    version = 'default config'
    refresh_interval = 5
    heads_up_threshold = 7
    default_threshold = 10
    aggression_index = 7
    safety_index = 4
    check_three_of_a_kind = False
    three_of_a_kind_with_two_cards_in_hand_bet = 10000
    three_of_a_kind_with_one_card_in_hand_bet = 10000
    check_two_pairs = False
    two_pair_bet = 10000
    check_four_of_a_kind = False
    four_of_a_kind_bet = 10000
    check_flush = False
    flush_bet = 10000

    def __init__(self):
        self.log = player.log
        self._start_thread()

    @staticmethod
    def get_instance(*args, **kwargs):
        global config_instance

        if config_instance is None:
            config_instance = Config(*args, **kwargs)

        return config_instance

    def load(self):
        try:
            client = MongoClient(MONGO_JSON_URL,ssl_cert_reqs=ssl.CERT_NONE)

            config_json = client.config.config.find_one({})

            for k, v in config_json.iteritems():
                self.__setattr__(k, v)
                self.log.info('config set %s = %s', k, v)

            self.log.info('finished loading config file')
        except Exception as e:
            self.log.error('exception caught: %s', e)

    def _start_thread(self):
        thread = threading.Thread(target=self._load)
        thread.start()

    def _load(self):
        while True:
            self.load()
            time.sleep(self.refresh_interval)
