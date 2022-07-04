import json

from flask import request, current_app, make_response, render_template
from flask_restful import Resource
from sqlalchemy.sql import text as sql_text

from utils.utils import ConfigsParser as config
from classes.pearl import Pearl

class Prices(Resource):
    def __init__(self):
        self.log = current_app.logger
        self.log.info("Initiating Prices app ...")
        self.pearl = Pearl()
        self.configs = config.parse_configs('PRICES')
        self.db, self.db_session = self.pearl.get_db_session()
        self.connection = self.db.engine.connect()

    
    def __del__(self):
        self.log.info("destroying the prices app...")

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
        response = self.router(reqparam, message)
        return response

    def post(self,reqparam):
        price_data = request.get_json()
        self.log.info("Received price post data, {}".format(price_data))
        response = self.router(reqparam, price_data)
        return response
    
    def router(self, reqparam,message):
        if reqparam == "get_prices":
            response = self.get_prices(message)
            return response
        
        elif reqparam == "add_prices":
            response = self.add_prices(message)
            return response
        
        elif reqparam == "get_price_details":
            response = self.get_price_details(message)
            return response
        
        else:
            response = "Unknown route, {}".format(reqparam)
            return response

    def get_prices(self,message):
        self.log.info("Fetching prices ....")
        try:
            select_query = "select price_id, buying_price, selling_price from prices"
            result = self.connection.execute(sql_text(select_query)).fetchall()
            prices = [dict(row) for row in result]
            temp_price = json.dumps(prices, indent=4, sort_keys=True, default=str)
            prices = json.loads(temp_price)
            
            self.log.info("prices are: {}".format(prices))
            return prices

        except Exception as e:
            self.log.error("Could not fetch prices due to error: {}".format(e))      
            return "Could not fetch prices due to error: {}".format(e)      

    def get_price_details(self, id):
        self.log.info("Fetching price details for id: {}",id)
        try:
            select_query = "select * from prices where price_id= :price_id"
            data ={
                "price_id":id.get("price_id")
            }

            resp = self.connection.execute(sql_text(select_query),data).fetchone()
            resp_dict = dict(resp)
            temp_resp = json.dumps(resp_dict, indent=4, sort_keys=True, default=str)
            result = json.loads(temp_resp)
            self.log.info("The result is, {}".format(result))
            return result
        
        except Exception as e:
            self.log.error("Could not fetch price details due to error: {}".format(e))
            return "Could not fetch price details due to error: {}".format(e)


    def add_prices(self, price_data):
        self.log.info("Adding price data,{}", format(price_data))
        try:
            insert_query = "insert into prices(buying_price,selling_price) values(:buying_price,:selling_price)"
            for line in price_data:
                data = {
                    "buying_price":line.get("buying_price"),
                    "selling_price":line.get("selling_price")
                }
            resp = self.connection.execute(sql_text(insert_query), data)
            self.log.info("The price add response is, {}".format(resp))
            return "Successfully added"

        
        except Exception as e:
            self.log.error("Could not add the price data due to the error,{}",format(e))
            return "Could not add the price data due to the error,{}",format(e)