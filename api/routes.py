from flask import Blueprint, current_app, request, jsonify
from assets.extensions import mongo
from pprint import pprint
from assets.decors import errorhandler, getaddress

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/getit", methods=["GET"])
@errorhandler
@getaddress
def getit():

    return jsonify({"success": True}), 200
