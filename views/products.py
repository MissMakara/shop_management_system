import json

from flask import current_app, request, make_response, render_template
from flask_restful import Resource
from sqlalchemy.sql import text as sql_text

from utils.utils import ConfigsParser as config
from classes.pearl import Pearl

class Products(Resource):
    def __init__(self):
        self.log = current_app.logger
        self.log.info("Products app initializing")
        self.pearl = Pearl()
        self.configs = config.parse_configs('PRODUCTS')
        self.db, self.db_session = self.pearl.get_db_session()
        self.connection = self.db.engine.connect()

    def __del__(self):
        self.log.info("Destroying products app")
        if self.configs:
            self.configs = None

        if self.connection:
            self.db.close()

        if self.db_session:
            self.db_session.close()

        if self.db:
            self.db.close()

        
    def get(self, reqparam):
        message = request.args.to_dict()
        response = self.router(reqparam,message)
        return response
    

    def post(self, reqparam):
        message = request.get_json()
        self.log.info("Received products post request..{}".format(message))
        response = self.router(reqparam, message)
        return response

    def router(self, reqparam, message):
        if reqparam == "get_products":
            response = self.get_products(message)
            return response

        elif reqparam == "add_products":
            response =  self.add_products(message)
            return response
        
        elif reqparam == "get_product_details":
            response = self.get_product_details(message)
            return response
        
        else:
            response = "Unknown route {}".format(reqparam)
            return response

    def get_products(self, message):
        self.log.info("received request to fetch product details")
        try:
            select_query = "select BIN_TO_UUID(product_id) product_id, product_name,BIN_TO_UUID(category_id) category_id from products order by product_id"
            result = self.connection.execute(sql_text(select_query)).fetchall()
            products = [dict(row) for row in result]
            temp_products = json.dumps(products, indent=4,sort_keys=True, default=str)
            products = json.loads(temp_products)
            self.log.info("Products are: {}".format(products))
            return products
        
        except Exception as e:
            self.log.error("Unable to get products due to: {}".format(e))
            return None

    def get_product_details(self,id):
        self.log.info("Fetching product details for product id {}".format(id))
        try:
            select_query = "select BIN_TO_UUID(product_id) product_id, product_name,category_id from products where product_id = :product_id"
            data ={
                "product_id":id.get('product_id')
            }
            res = self.connection.execute(sql_text(select_query), data).fetchone()
            temp_res = dict(res)
            temp_res_2 = json.dumps(temp_res, indent =4, sort_keys=True, default =str)
            result = json.loads(temp_res_2)
            self.log.info("The result is {}".format(result))
            return result
        
        except Exception as e:
            self.log.error("Unable to fetch product details due to error: {}".format(e))
            return "Unable to fetch product details due to error: {}".format(e)


    def add_products(self,products_data):
        self.log.info("Adding product information... {}".format(products_data))
        try:
            insert_query = "insert into products(description,price_id,product_name,quantity) values(:description,:price_id,:product_name,:quantity)"
            for line in products_data:

                data = {
                    "description":line.get("description"),
                    "price_id":line.get("price_id"),
                    "product_name":line.get("product_name"),
                    "quantity":line.get("quantity")

                }
                resp = self.connection.execute(sql_text(insert_query), **data)
            
            self.log.info("Response  is {}".format(resp))
            return "Successfully added"
        
        except Exception as e:
            self.log.error("Could not add to products table due to the error: {}".format(e))
            return "Could not add to products table due to the error: {}".format(e)
            
