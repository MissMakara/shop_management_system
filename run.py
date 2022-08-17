import logging.handlers

from concurrent_log_handler import ConcurrentRotatingFileHandler
from flask import Flask
from flask_restful import Api

from utils.utils import ConfigsParser as config
from views.main import home
from views.categories import Category
from views.products import Products
from views.prices import Prices
from views.orders import Orders
from views.destinations import Destinations
from views.customers import Customers
from views.users import Users



configs = config.parse_configs('BASE')

handler = ConcurrentRotatingFileHandler(configs.get('log_file'), "a", 1024 * 1024 * 1024 * 1, 1000)
formatter = logging.Formatter(
    '%(asctime)s] - %(name)s - %(levelname)s in %(module)s:%(lineno)d:%(funcName)-10s %(message)s')
handler.setFormatter(formatter)


app = Flask(__name__)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

api = Api(app)

#endpoints
app.add_url_rule("/", view_func= home)
api.add_resource(Category, "/categories/<string:reqparam>")
api.add_resource(Products, "/products/<string:reqparam>")
api.add_resource(Prices, "/prices/<string:reqparam>")
api.add_resource(Orders,"/orders/<string:reqparam>")
api.add_resource(Customers, "/customers/<string:reqparam>")
api.add_resource(Destinations, "/destinations/<string:reqparam>")
api.add_resource(Users, "/users/<string:reqparam>")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
