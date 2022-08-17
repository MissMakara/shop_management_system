import json
import uuid

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
            # select_query = "select BIN_TO_UUID(orders.order_id) order_id, customers.first_name, customers.last_name, destinations.destination_name, customer_destinations.destination_details,orders.total_amount as total ,orders.discount ,orders.final_amount as final "\
            #     "from orders INNER JOIN customers on orders.customer_id = customers.customer_id INNER JOIN customer_destinations on orders.customer_destination_id  = customer_destinations.customer_destination_id INNER JOIN destinations on customer_destinations.destination_id = destinations.destination_id order by orders.order_id"
            
            select_query = "select BIN_TO_UUID(o.order_id) order_id, c.first_name, c.last_name,BIN_TO_UUID(op.product_id) product_id, op.product_quantity,d.destination_name, cd.destination_details, o.total_amount as total ,o.discount ,o.final_amount as final "\
            "from orders o inner join customer_destinations cd on o.customer_destination_id = cd.customer_destination_id inner join destinations d on cd.destination_id = d.destination_id inner join customers c on o.customer_id=c.customer_id inner join order_product op on o.order_id = op.order_id"

            result = self.connection.execute(sql_text(select_query)).fetchall()
            orders = [dict(row) for row in result]
            temp_orders = json.dumps(orders, indent=4, sort_keys=True, default=str)
            orders = json.loads(temp_orders)
            
            self.log.info("Orders are: {}".format(orders))
            return orders

        except Exception as e:
            self.log.error("Unable to fetch orders due to: {}".format(e))
            return None
    
    def get_order_product_details(self,message):
        self.log.info("getting order product details...")
        try:
            select_query = "select BIN_TO_UUID(order_product_id) order_product_id from order_product"
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
            select_query = "select BIN_TO_UUID(order_id) order_id, from orders where order_id = :order_id"
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
           
            insert_query1 = "insert into orders (order_id, customer_id, order_status) values (UUID_TO_BIN(:order_id), UUID_TO_BIN(:customer_id), :status)"
            insert_query2 = "insert into order_product (order_product_id, order_id, product_id, price, product_quantity) values(UUID_TO_BIN(:order_product_id),UUID_TO_BIN(:order_id),UUID_TO_BIN(:product_id),:price, :product_qtty)"
            insert_query3 = "update orders set total_amount =:total_amount, discount=:discount, final_amount= :final_amount, customer_destination_id = UUID_TO_BIN(:cust_dest_id), payment_reference=:payment_reference, additional_details=:additional_details where order_id =UUID_TO_BIN(:order_id)"
            
            orderid = str(uuid.uuid4())
            self.log.info("order_id is {}".format(orderid))
           
    
            data1 = {
                "order_id":orderid,
                "customer_id":order_data["customer_id"],
                "status": order_data["order_status"]
            }
            
            # import pdb
            # pdb.set_trace()
            resp1 = self.connection.execute(sql_text(insert_query1), data1)

            self.log.info("step 1: First insert into Orders done. Response is: {}".format(resp1))
            products_data = order_data['products']
            

            for line in products_data:
                orderproductid = str(uuid.uuid4())

                data2 = {
                    "order_product_id": orderproductid,
                    "order_id": orderid,
                    "product_id":line["product_id"],
                    "price":line["price"],
                    "product_qtty":line["product_qtty"]
                }

            resp2 = self.connection.execute(sql_text(insert_query2), data2)
            self.log.info("STEP 2:Insert into order_products done. Response is: {}".format(resp2))

            
            data3 ={
                "order_id":orderid,
                "total_amount":order_data['total_amount'],
                "discount":order_data.get("discount"),
                "final_amount":order_data["final_amount"],
                "cust_dest_id":order_data["customer_destination_id"],
                "payment_reference":order_data.get("payment_reference"),
                "additional_details":order_data.get("additional_details")
            }

            resp3 = self.connection.execute(sql_text(insert_query3), data3)
            self.log.info("STEP 3: Second inserts into Orders done. Response is, {}".format(resp3))
            
            return "Order successfully added"

        
        except Exception as e:
            self.log.error("Could not add the order data due to the error,{}",format(e))
            return "Could not add the order data due to the error,{}",format(e)  
             
   
    #update order view
    #update order based on order_id, change order_status, add payment reference, 
    # add additional details, can't remove from additional details

   