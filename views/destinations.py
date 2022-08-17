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
        
    def get(self,reqparam):
        message = request.args.to_dict()
        response = self.router(reqparam,message)
        return response

    def post(self,reqparam):
        dest_data = request.get_json()
        self.log.info("Received destinations post request,{}", dest_data)
        response = self.router(reqparam,dest_data)
        return response
    
    def router(self, reqparam, message):
        if reqparam == "get_destinations":
            response = self.get_destinations(message)
            return response

        elif reqparam == "add_destination":
            response = self.add_destination(message)
            return response
        
        elif reqparam == "get_destination_details":
            response = self.get_destination_details(message)
            return response
        
        elif reqparam == "get_customer_destination_details":
            response = self.get_customer_destinations(message)
            return response

        else:
            response = "Unkown route, {}".format(reqparam)
            return response
        

    def get_destinations(self,message):
        self.log.info("Fetching destinations ....")
        try:
            select_query = "select BIN_TO_UUID(destination_id) destination_id, destination_name, delivery_charge from destinations"
            result = self.connection.execute(sql_text(select_query)).fetchall()
            destinations = [dict(row) for row in result]
            temp_dest = json.dumps(destinations, indent=4, sort_keys=True, default=str)
            destinations = json.loads(temp_dest)
            self.log.info("destinations are: {}".format(destinations))
            return destinations

        except Exception as e:
            self.log.error("Could not fetch destinations due to error: {}".format(e))

    def get_customer_destinations(self,message):
        self.log.info("Fetching customer destinations ....")
        try:
            select_query = "select customers.first_name, customers.last_name, BIN_TO_UUID(customer_destinations.customer_destination_id) customer_destination_id, BIN_TO_UUID(customer_destinations.customer_id) customer_id, BIN_TO_UUID(customer_destinations.destination_id) destination_id, destinations.destination_name, customer_destinations.destination_details "\
                "from customer_destinations INNER JOIN destinations on customer_destinations.destination_id=destinations.destination_id INNER JOIN customers on customer_destinations.customer_id = customers.customer_id"
            result = self.connection.execute(sql_text(select_query)).fetchall()
            destinations = [dict(row) for row in result]
            temp_dest = json.dumps(destinations, indent=4, sort_keys=True, default=str)
            destinations = json.loads(temp_dest)
            self.log.info("customer destinations are: {}".format(destinations))
            return destinations

        except Exception as e:
            self.log.error("Could not fetch customer destinations due to error: {}".format(e))


    def add_destination(self, dest_data):
        self.log.info("Adding destination data, {}".format(dest_data))
        try:
            insert_query = "insert into destinations(destination_name,delivery_charge) values(:destination_name,:delivery_charge)"
            for line in dest_data:

                data = {
                    "destination_name":line.get("destination_name"),
                    "delivery_charge":line.get("delivery_charge")
                }
            
            resp = self.connection.execute(sql_text(insert_query), data)
            self.log.info("The resp is {}".format(resp))
            return "Successfully added"
        
        except Exception as e:
            self.log.error("Could not insert destination information due to error, {}".format(e))
            return "Could not insert destination information due to error, {}".format(e)


    def get_destination_details(self,id):
        self.log.info("Fetching destination details for id {}".format(id))
        try:
            select_query = "select * from destinations where destination_id = :destination_id"
            data = {
                "destination_id":id.get("destination_id")

            }
            resp = self.connection.execute(sql_text(select_query),data).fetchone()
            temp_res= dict(resp)
            result = json.loads(json.dumps(temp_res, indent =4, sort_keys=True, default =str))
            self.log.info("The result is {}".format(result))
            return result
        
        except Exception as e:
            self.log.error("Could not fetch destination details due to error: {}".format(e))
            return "Could not fetch destination details due to error: {}".format(e)
