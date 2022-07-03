import json

from flask import request, current_app, make_response, render_template
from flask_restful import Resource
from sqlalchemy.sql import text as sql_text


from utils.utils import ConfigsParser as config
from classes.pearl import Pearl

class Destinations(Resource):
    def __init__(self):
        self.log = current_app.logger
        self.log.info("Initiating Destinations app ...")
        self.pearl = Pearl()
        self.configs = config.parse_configs('DESTINATIONS')
        self.db, self.db_session = self.pearl.get_db_session()
        self.connection = self.db.engine.connect()

    
    def __del__(self):
        self.log.info("destroying the destinations app...")

        if self.configs:
            self.configs = None
        
        if self.db_session:
            self.db_session.remove()
        
        if self.connection:
            self.db.close()

        if self.db:
            self.db.close()
        
    def get(self):
        response = self.get_destinations()
        return response

    def get_destinations(self):
        self.log.info("Fetching destinations ....")
        try:
            select_query = "select * from destinations"
            result = self.connection.execute(sql_text(select_query)).fetchall()
            destinations = [dict(row) for row in result]
            temp_dest = json.dumps(destinations, indent=4, sort_keys=True, default=str)
            destinations = json.loads(temp_dest)
            self.log.info("destinations are: {}".format(destinations))
            return destinations

        except Exception as e:
            self.log.error("Could not fetch destinations due to error: {}".format(e))

    
    def post(self):
        dest_data = request.get_json()
        self.log.info("Received destinations post request,{}", dest_data)
        response = self.add_destinations(dest_data)
        return response

    def add_destinations(self, dest_data):
        self.log.info("Adding destination data, {}".format(dest_data))
        try:
            insert_query = "insert into destinations(destination_name,delivery_charge) values(:destination_name,:delivery_charge)"
            resp = self.connection.execute(sql_text(insert_query), dest_data)
            self.log.info("The resp is {}".format(resp))
            return "Successfully added"
        
        except Exception as e:
            self.log.error("Could not insert destination information due to error, {}".format(e))
            return "Could not insert destination information due to error, {}".format(e)

