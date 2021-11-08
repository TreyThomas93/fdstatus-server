from flask import Blueprint, current_app, request, jsonify
from assets.extensions import mongo
from trestle import Trestle
from pprint import pprint
from assets.decors import errorhandler, getaddress

trestle = Trestle()

app_api = Blueprint("app/api", __name__, url_prefix="/app/api")

# 282195054

@app_api.route("/getPropertyByKey", methods=["GET"])
@errorhandler
def getPropertyByKey():

    listing_key = request.args.get("listing_key")
    
    if listing_key == None or listing_key == "":

        current_app.logger.warning("missing listing key")

        return jsonify({"error": "missing listing key"}), 400

    url = f"{trestle.base_url}/Property?$filter=ListingKey eq '{listing_key}'"
    
    resp = trestle.sendRequest(url)

    listing = resp.json()['value'] if "value" in resp.json() else resp.json()

    return jsonify({"listing": listing}), 200


@app_api.route("/getImagesByKey", methods=["GET"])
@getaddress
@errorhandler
def getImagesByKey():
    
    listing_key = request.args.get("listing_key")
    
    if listing_key == None or listing_key == "":

        current_app.logger.warning("missing listing key")

        return jsonify({"error": "missing listing key"}), 400

    url = f"{trestle.base_url}/Media?$filter=ResourceRecordKey eq '{listing_key}'&$orderby=Order"
    
    resp = trestle.sendRequest(url)
    
    images = resp.json()['value'] if "value" in resp.json() else resp.json()
    
    return jsonify({"images": images}), 200

