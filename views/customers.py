import json

from classes.pearl import Pearl
from flask import current_app, make_response, render_template, request
from flask_restful import Resource
from sqlalchemy.sql import text as sql_text
from utils.utils import ConfigsParser as config


class Customers(Resource):
    def __init__(self):
        self.log = current_app.logger
        self.log.info("Initiating Customers app ...")
        self.pearl = Pearl()
        self.configs = config.parse_configs('CUSTOMERS')
        self.db, self.db_session = self.pearl.get_db_session()
        self.connection = self.db.engine.connect()

    
    def __del__(self):
        self.log.info("destroying the customers app...")

        if self.configs:
            self.configs = None
        
        if self.db_session:
            self.db_session.remove()
        
        if self.connection:
            self.db.close()

        if self.db:
            self.db.close()
        
    def get(self, reqparam):
        message = request.args.to_dict()
        response = self.router(reqparam, message)
        return response

    def post(self, reqparam):
        message =request.get_json(force=True)
        self.log.info("Received customers post request..{}".format(message))
        response = self.router(reqparam, message)
        return response
        # return "success"

    def router(self, reqparam, message):
        if reqparam == "list_customers":
            response = self.get_customers(message)
            return response
        
        elif reqparam == "get_customer_details":
            response = self.get_customer_details(message)
            return response

        elif reqparam == "add_customers":
            response = self.add_customers(message)
            return response
        
        else:
            response = "Unknown route, {}".format(reqparam)
            return response


    def add_customers(self, customer_data):
        self.log.info("Adding customer data, {}".format(customer_data))
        try:
            insert_query = "insert into customers(contact, first_name,last_name,destination_id) values(:contact,:first_name,:last_name,:destination_id)"

            for line in customer_data:
                data = {
                    "contact":line.get("contact"),
                    "first_name":line.get("first_name"),
                    "last_name":line.get("last_name"),
                    "destination_id":line.get("destination_id")
                }
            
                resp = self.connection.execute(sql_text(insert_query),**data)
            # sqlalchemy.engine.base.Connection.execute() argument after ** must be a mapping, not str"
            
            self.log.info("Resp output is {}".format(resp))
            return "Successfully added"


        except Exception as e:
            self.log.error("Could not add customer data due to error,{}".format(e))
            return "Could not add customer data due to error,{}".format(e)


    def get_customers(self, message):
        self.log.info("Fetching customers ....")
        try:
            select_query = "select BIN_TO_UUID(customer_id) customer_id, contact, first_name, last_name from customers order by 1"
            result = self.connection.execute(sql_text(select_query)).fetchall()
            self.log.info("customers are: {}".format(result))
            customers = [dict(row) for row in result]
            temp_customers = json.dumps(customers, indent=4, sort_keys=True, default=str)
            final_customers = json.loads(temp_customers)
            self.log.info("customers are: {}".format(final_customers))
            return final_customers

        except Exception as e:
            self.log.error("Could not fetch customers due to error: {}".format(e))

    
    def get_customer_details(self, id):
        self.log.info("Fetching customer details for customer id {}".format(id))
        try:
            cust_id = id.get("customer_id")
            self.log.info("received customer_id, {}".format(cust_id))
            select_query = "select BIN_TO_UUID(customers.customer_id) customer_id, customers.contact, customers.first_name, customers.last_name, destinations.destination_name, customer_destinations.destination_details "\
                 "from customers INNER JOIN customer_destinations on customers.customer_id = customer_destinations.customer_id INNER JOIN destinations on customer_destinations.destination_id = destinations.destination_id"
            
            data = {
                "customer_id":cust_id
            }
            # self.log.info("received response, {}".format(resp))
            resp = self.connection.execute(sql_text(select_query),data).fetchone()
            self.log.info("received response, {}".format(resp))
            details = dict(resp)
            self.log.info("The resp is {}".format(details))
            return details
        
        except Exception as e:
            self.log.error("Could not fetch customer details due to error {}".format(e))
            return "Could not fetch customer details for id due to error {}".format(e)
