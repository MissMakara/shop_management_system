import json

from email import message
from flask import current_app,request, make_response,render_template
from flask_restful import Resource
from sqlalchemy.sql import text as sql_text

from utils.utils import ConfigsParser as config
from classes.pearl import Pearl

class Category(Resource):
    def __init__(self):
        self.log = current_app.logger
        self.log.info("Category app init")
        self.pearl = Pearl()
        self.configs = config.parse_configs('CATEGORIES')
        self.db, self.db_session = self.pearl.get_db_session()
        self.connection = self.db.engine.connect()
        

    def __del__(self):
        self.log.info("Destroying categories app")
        if self.configs:
            self.configs = None
        
        if self.connection:
            self.db.close()

        if self.db_session:
            self.db.close()

        if self.db:
            self.db.close()

    
    def get(self, reqparam):
        message = request.args.to_dict()
        response = self.router(reqparam, message)
        return response

    def post(self, reqparam):
        message = request.get_json()
        self.log.info("Received post request {}".format(message))
        response = self.router(reqparam, message)
        return response
    
    def router(self, reqparam, message):
        if reqparam == "list_categories":
            response = self.get_categories(message)
        
        elif reqparam == "fetch_category":
            response = self.get_category(message)

        elif reqparam == "add_categories":
            response = self.add_categories(message)

        # elif reqparam == "add_category":
        #     response = self.add_category(message)

        else:
            response = "Unknown route: {}".format(reqparam)

        return response  



    def get_categories(self, message):
        self.log.info("received request to list categories")
        try:
            select_query = "select BIN_TO_UUID(category_id) category_id, category_name,BIN_TO_UUID(parent_id) parent_id from categories order by 1"
            result = self.connection.execute(sql_text(select_query)).fetchall()
            categories = [dict(row) for row in result]
            cat_temp = json.dumps(categories, indent=4, sort_keys=True, default=str)
            cat = json.loads(cat_temp)
            self.log.info("final categories are: {}".format(cat))
            return cat

        except Exception as e:
            self.log.error("Unable to get categories due to: {}".format(e))
            return None

   
    def get_category(self, message):
        try:
            category_id = message["id"]
            #learn on various ways to fetch data from dicts

            self.log.info("received request to fetch category:{}".format(category_id))
            select_query = "select category_id, category_name from categories where category_id = :category_id"
            data = {
                "category_id": category_id
            }
            resp = self.connection.execute(sql_text(select_query),data).fetchone()
            category = dict(resp)
            self.log.info("Received category: {}".format(category))
            return category
    
            #create routes for all views
            #select individual items based on id
            #create your own dict for all views   
 
        except Exception as e:
            self.log.error("Unable to get category due to: {}".format(e))
            return None
    

    def add_categories(self, cat_data):
        self.log.info("Adding categories ...{}".format(cat_data))
        try:
            insert_query ="insert into categories (category_name) values (:category_name)"

         
            for line in cat_data:
                data = {
                    "category_name":line["category_name"]
                }
                resp = self.connection.execute(sql_text(insert_query), **data)

            #resp = self.connection.execute(sql_text(insert_query), cat_data)
            self.log.info("Resp output ...{}".format(resp))
            return "Successfully added"

        except Exception as e:
            self.log.error("Could not add categories due to error {}".format(e))
            return "Could not add categories due to error {}".format(e)




    # def add_category(self, cat_data):
    #     self.log.info("Adding category ...{}".format(cat_data))
    #     try:
    #         insert_query ="insert into category (category_name) values (:category_name)"

    #         #for line in cat_data:
    #         #self.connection.execute(sql_text(insert_query), **line)
    #         resp = self.connection.execute(sql_text(insert_query), cat_data)
    #         self.log.info("Resp output ...{}".format(resp))
    #         return "Successfully added"

    #     except Exception as e:
    #         self.log.error("Could not add category due to error {}".format(e))
    #         return "Could not add category due to error {}".format(e)

