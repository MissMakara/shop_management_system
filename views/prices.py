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
        
    def get(self):
        response = self.get_prices()
        return response

    def get_prices(self):
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

    
    def post(self):
        price_data = request.get_json()
        self.log.info("Received price post data, {}".format(price_data))
        response = self.add_prices(price_data)
        return response
    
    def add_prices(self, price_data):
        self.log.info("Adding price data,{}", format(price_data))
        try:
            insert_query = "insert into prices(buying_price,selling_price) values(:buying_price,:selling_price)"
            resp = self.connection.execute(sql_text(insert_query), price_data)
            self.log.info("The price add response is, {}".format(resp))
            return "Successfully added"

        
        except Exception as e:
            self.log.error("Could not add the price data due to the error,{}",format(e))
            return "Could not add the price data due to the error,{}",format(e)