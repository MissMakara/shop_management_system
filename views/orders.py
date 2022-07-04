from urllib import response
from flask import current_app, request, make_response, render_template
from flask_restful import Resource
from sqlalchemy.sql import text as sql_text
import simplejson as json

from utils.utils import ConfigsParser as config
from classes.pearl import Pearl

class Orders(Resource):
    def __init__(self):
        self.log = current_app.logger
        self.log.info("Initializing Orders app...")
        self.pearl = Pearl()
        self.configs = config.parse_configs('ORDERS')
        self.db, self.db_session = self.pearl.get_db_session()
        self.connection = self.db.engine.connect()

    
    def __del__(self):
        self.log.info("Destroying Orders app....")
        if self.configs:
            self.configs = None
        
        if self.connection:
            self.db.close()

        if self.db_session:
            self.db_session.remove()
        
        if self.db:
            self.db.close()

    

    def get(self, reqparam):
        message = request.args.to_dict()
        response = self.router(reqparam, message)
        return response
    
        
    def post(self,reqparam):
        order_data = request.get_json()
        self.log.info("Received order post data, {}".format(order_data))
        response = self.router(reqparam, order_data)
        return response

    def router(self,reqparam, message):
        if reqparam == "get_orders":
            response = self.get_orders(message)
            return response
        
        elif reqparam == "get_order_details":
            response = self.get_order_details(message)
            return response
        
        elif reqparam == "add_order":
            response = self.add_order(message)
            return response


    def get_orders(self,message):
        self.log.info("getting orders...")
        try:
            select_query = "select * from orders order by order_id"
            result = self.connection.execute(sql_text(select_query)).fetchall()
            orders = [dict(row) for row in result]
            temp_orders = json.dumps(orders, indent=4, sort_keys=True, default=str)
            orders = json.loads(temp_orders)
            
            self.log.info("Orders are: {}".format(orders))
            return orders

        except Exception as e:
            self.log.error("Unable to fetch orders due to: {}".format(e))
            return None

    def get_order_details(self,message):
        self.log.info("Fetching order data for id,{}".format(message))
        try:
            select_query = "select * from orders where order_id = :order_id"
            data ={
                "order_id":message.get("order_id")
            }
            resp = self.connection.execute(sql_text(select_query),data).fetchone()
            resp_dict =dict(resp)
            self.log.info("Resp dict is {}".format(resp_dict))
            temp_resp = json.dumps(resp_dict, indent=4, sort_keys=True, default=str)
            result = json.loads(temp_resp)
            self.log.info("The result is: {}".format(result))
            return result
        
        except Exception as e:
            self.log.error("Could not fetch order details due to error: {}".format(e))
            return "Could not fetch order details due to error: {}".format(e)
    
    def add_order(self, order_data):
        self.log.info("Adding order data,{}". format(order_data))
        try:
            insert_query = "insert into orders(customer_id,discount,final_amount,order_product,order_status,payment_reference,additional_details,total_amount) values(:customer_id,:discount,:final_amount,:order_product,:order_status,:payment_reference,:additional_details,:total_amount)"
            for line in order_data:
                data ={
                    "customer_id":line.get("customer_id"),
                    "discount":line.get("discount"),
                    "final_amount":line.get("final_amount"),
                    "order_product":line.get("order_product"),
                    "order_status":line.get("order_status"),
                    "payment_reference":line.get("payment_reference"),
                    "additional_details":line.get("additional_details"),
                    "total_amount":line.get("total_amount")
                }

            resp = self.connection.execute(sql_text(insert_query), data)
            self.log.info("The order add response is, {}".format(resp))
            return "Order successfully added"

        
        except Exception as e:
            self.log.error("Could not add the order data due to the error,{}",format(e))
            return "Could not add the order data due to the error,{}",format(e)  
             
   


   