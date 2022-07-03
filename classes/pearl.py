from flask import current_app
from db.connection import Db
from utils.utils import ConfigsParser as configs 


class Pearl(object):
    def __init__(self):
        self.log = current_app.logger
        self.log.info("creating pearl object")
        self.db_configs = configs.parse_configs('DATABASE')
        self.db, self.db_session = self.get_db_session()
        self.connection = self.db.engine.connect()

    def __del__(self):
        self.log.info("destroying pearl object")
        if self.db_configs:
            self.db_configs = None
        
        if self.connection:
            self.db.close()
        
        if self.db_session:
            self.db_session.remove()
        
        if self.db:
            self.db.close()


    def get_db_session(self):
        self.db = Db(self.db_configs['host'], self.db_configs['db_name'],
                     self.db_configs['username'],
                     self.db_configs['password'], port=self.db_configs['port'])

        self.db_session = self.db.get_db_session()
        return self.db, self.db_session

    