from flask import Blueprint
from flask_restx import Api

from .entrepreneur import api as entrepreneur

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(
    blueprint,
    title="Census API ETL",
    version="1.0",
    description="Some of the Census APIs transformed",
)

api.add_namespace(entrepreneur)
