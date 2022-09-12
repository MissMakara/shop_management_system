import json
import uuid

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
        
        # elif reqparam == "get_category_products":
        #     response = self.get_category
        
        else:
            response = "Unknown route {}".format(reqparam)
            return response

    def get_products(self, id):
        self.log.info("received request to fetch product details")
        try:
            select_query = "select BIN_TO_UUID(products.product_id) parent_product_id, products.product_name,categories.category_name as category, BIN_TO_UUID(products.category_id) as category_id ,BIN_TO_UUID(product_colours.product_colour_id) product_colour_id, product_colours.primary_colour as colour, product_colours.quantity as quantity, BIN_TO_UUID(products.price_id) price_id, prices.selling_price as price "\
                "from products INNER JOIN categories on products.category_id = categories.category_id INNER JOIN product_colours on products.product_id = product_colours.product_id INNER JOIN prices on products.price_id = prices.price_id ORDER BY categories.category_name ASC"
            
            select_query_desc = "select BIN_TO_UUID(products.product_id) parent_product_id, products.product_name,categories.category_name as category, BIN_TO_UUID(products.category_id) as category_id ,BIN_TO_UUID(product_colours.product_colour_id) product_colour_id, product_colours.primary_colour as colour, product_colours.quantity as quantity, BIN_TO_UUID(products.price_id) price_id, prices.selling_price as price "\
                "from products INNER JOIN categories on products.category_id = categories.category_id INNER JOIN product_colours on products.product_id = product_colours.product_id INNER JOIN prices on products.price_id = prices.price_id ORDER BY categories.category_name DESC"
            

            data = {
                "limit":id.get('limit'),
                "page":id.get('page'),
                "sort":id.get('sort')
            }
            page = int(data.get('page'))
            limit = int(data.get('limit'))
            sorting = data.get('sort')
            start = (page-1)*limit
            stop = limit * page

            # import pdb
            # pdb.set_trace()
            
            if sorting == 'ASC':
                result = self.connection.execute(sql_text(select_query)).fetchall()
            if sorting == 'DESC':
                result = self.connection.execute(sql_text(select_query_desc)).fetchall()

            initial_products = [dict(row) for row in result]
            # import pdb
            # pdb.set_trace()

            products = initial_products[start:stop]

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
            select_query = "select BIN_TO_UUID(products.product_id) parent_product_id, products.product_name,categories.category_name, BIN_TO_UUID(products.price_id) price_id, BIN_TO_UUID(products.category_id) as category_id ,BIN_TO_UUID(product_colours.product_colour_id) product_colour_id, product_colours.primary_colour as colour, product_colours.quantity as quantity, prices.selling_price as price "\
                "from products INNER JOIN categories on products.category_id = categories.category_id INNER JOIN product_colours on products.product_id = product_colours.product_id INNER JOIN prices on products.price_id = prices.price_id where products.product_id = UUID_TO_BIN(:product_id)"
        
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
            uuid_val = str(uuid.uuid4())
            # import pdb
            # pdb.set_trace()
            self.log.info("uuid value is {}".format(uuid_val))

            insert_query = "insert into products(product_id, description, price_id, product_name, category_id) "\
                "values(UUID_TO_BIN(:uuid),:description,UUID_TO_BIN(:price_id),:product_name, UUID_TO_BIN(:category_id))"

            

            for line in products_data:
                data = {
                    "uuid": uuid_val,
                    "description":line.get("product_description"),
                    "price_id":line.get("price"),
                    "product_name":line.get("product_name"),
                    "category_id":line.get("category")
                }


                self.log.info("Running insert")
                resp = self.connection.execute(sql_text(insert_query), data)
                self.log.info("Product entry response  is {}".format(resp))

                trx_id = uuid_val
                self.log.info("The last transaction id is {}".format(trx_id))

                data2 = {
                    "transaction_id":trx_id,
                    "secondary_colour": line.get("secondary_colour"),
                    "primary_colour": line.get("primary_colour"),
                    "quantity": line.get("quantity")
                }

                colours_insert_query = "INSERT INTO product_colours(product_colour_id, product_id, primary_colour, secondary_colour, quantity) "\
                "VALUES (UUID_TO_BIN(UUID()), UUID_TO_BIN(:transaction_id),:primary_colour,:secondary_colour, :quantity)"  

                resp2 = self.connection.execute(sql_text(colours_insert_query), **data2)
                self.log.info("Colour entry response  is {}".format(resp2))

            self.log.info("Final Response  is {}".format(resp2))
            return "Successfully added"
        
        except Exception as e:
            self.log.error("Could not add to products table due to the error: {}".format(e))
            return "Could not add to products table due to the error: {}".format(e)
            
