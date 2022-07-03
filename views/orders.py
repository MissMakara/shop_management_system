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

    

    def get(self):
        response = self.get_orders()
        return response
    
    def get_orders(self):
        self.log.info("getting orders...")
        try:
            select_query = "select * from orders"
            result = self.connection.execute(sql_text(select_query)).fetchall()
            orders = [dict(row) for row in result]
            temp_orders = json.dumps(orders, indent=4, sort_keys=True, default=str)
            orders = json.loads(temp_orders)
            
            self.log.info("Orders are: {}".format(orders))
            return orders

        except Exception as e:
            self.log.error("Unable to fetch orders due to: {}".format(e))
            return None


    def post(self):
        order_data = request.get_json()
        self.log.info("Received order post data, {}".format(order_data))
        response = self.add_order(order_data)
        return response
    
    def add_order(self, order_data):
        self.log.info("Adding order data,{}", format(order_data))
        try:
            insert_query = "insert into orders(customer_id,discount,final_amount,order_product,order_status,payment_reference,additional_details,total_amount) values(:customer_id,:discount,:final_amount,:order_product,:order_status,:payment_reference,:additional_details,:total_amount)"
            resp = self.connection.execute(sql_text(insert_query), order_data)
            self.log.info("The order add response is, {}".format(resp))
            return "Order successfully added"

        
        except Exception as e:
            self.log.error("Could not add the order data due to the error,{}",format(e))
            return "Could not add the order data due to the error,{}",format(e)  
             
    # def add_order(self):
    #     self.log.info("adding orders ...")
    #     #a tuple of dictionaries of items to be added
        # data = ({
        #     "customer_id": 1,
        #     "order_product":,
        #     "total_amount":,
        #     "discount":,
        #     "final_amount":,
        #     "additional_details":,
        #     "order_status",
        #     "payment_reference":
        # })
        # try:
        #     insert_query ="INSERT INTO ORDERS
        #     (customer_id,order_product,total_amount,discount,final_amount,additional_details,order_status,payment_reference) 
        #     VALUES
        #     (:customer_id,:order_product,:total_amount,:discount,:final_amount,:additional_details,:order_status,:payment_reference)"

        #     for line in data:
        #         self.connection.execute(sql_text(insert_query), **line)

        # except Exception as e:
        #     self.log.info("Could not add order details due to error {}".format(e))






        



   