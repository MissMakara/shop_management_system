import json

from urllib import response
from uuid import UUID
from flask import current_app, request, make_response, render_template
from flask_restful import Resource
from sqlalchemy.sql import text as sql_text
import simplejson as json

from utils.utils import ConfigsParser as config
from classes.pearl import Pearl

class Users(Resource):
    def __init__(self):
        self.log = current_app.logger
        self.log.info("Initializing Users app...")
        self.pearl = Pearl()
        self.configs = config.parse_configs('USERS')
        self.db, self.db_session = self.pearl.get_db_session()
        self.connection = self.db.engine.connect()

    def __del__(self):
        self.log.info("destroying the users app...")

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
        self.log.info("Received users get request")
        response = self.router(reqparam,message)
        return response

    def post(self,reqparam):
        user_data = request.get_json()
        self.log.info("Received users post request,{}", user_data)
        response = self.router(reqparam,user_data)
        return response

    def router(self, reqparam, message):
        if reqparam == "get_users":
            response = self.get_users(message)
            return response

        elif reqparam == "add_users":
            response = self.add_user(message)
            return response
        
        elif reqparam == "get_user_details":
            response = self.get_user_details(message)
            return response

        else:
            response = "Unkown route, {}".format(reqparam)
            return response
        
    def get_users(self, message):
        self.log.info("Fetching users ....")
        try:
            select_query = "select BIN_TO_UUID(user_id) as user_id, user_name, first_name, last_name, user_role from users ORDER BY user_name ASC"
            
            select_query_desc = "select BIN_TO_UUID(user_id) as user_id, user_name, first_name, last_name, user_role from users order by user_name DESC"
            
            limit = int(message['limit'])
            page = int(message['page'])
            sorting = message.get('sort')
            start = (page-1)*limit
            stop = limit * page
            
            if sorting == 'ASC':
                result = self.connection.execute(sql_text(select_query)).fetchall()
            if sorting == 'DESC':
                result = self.connection.execute(sql_text(select_query_desc)).fetchall()
            
            user = [dict(row) for row in result]
            users = user[start:stop]
            temp_user = json.dumps(user, indent=4, sort_keys=True, default=str)
            users = json.loads(temp_user)
            self.log.info("users are: {}".format(users))

            return users

        except Exception as e:
            self.log.error("Could not fetch users due to error: {}".format(e))

    def get_user_details(self, message):
        self.log.info("Fetching user_id ".format(message))
  
        try:
            select_query = "select BIN_TO_UUID(user_id) as user_id, user_name, first_name,last_name, user_role "\
            "from users where user_id = UUID_TO_BIN(:user_id)"
        
            # import pdb
            # pdb.set_trace()
         
            data ={
                "user_id" : message.get('id')
            }
            
            result = self.connection.execute(sql_text(select_query), data).fetchall()
            user = [dict(row) for row in result]
            temp_user_dets = json.dumps(user, indent=4, sort_keys = True, default=str)
            user_details  = json.loads(temp_user_dets)
            self.log.info("user details are {}".format(user_details))
            return user_details
            

        except Exception as e:
            self.log.error("Could not fetch users due to error:{}".format(e))



    def add_user(self, user_data):
        self.log.info("Adding user data, {}".format(user_data))
        try:
            insert_query = "insert into users(user_id, first_name, last_name, user_name, user_role) values(UUID_TO_BIN(UUID()), :first_name,:last_name, :user_name, :user_role)"
            for line in user_data:
                data = {
                    "first_name":line.get("first_name"),
                    "last_name":line.get("last_name"),
                    "user_name":line.get("user_name"),
                    "user_role":line.get("user_role")
                }
            
            resp = self.connection.execute(sql_text(insert_query), data)
            self.log.info("The resp is {}".format(resp))
            return "Successfully added"
        
        except Exception as e:
            self.log.error("Could not insert user information due to error, {}".format(e))
            return "Could not insert user information due to error, {}".format(e)

