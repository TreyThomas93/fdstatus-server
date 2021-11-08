from flask import jsonify, current_app, request
import jwt
from functools import wraps
from assets.extensions import mongo


def errorhandler(fn):

    def wrapper(*args, **kwargs):

        try:

            return fn(*args, **kwargs)

        except Exception as e:

            current_app.logger.error(f"{fn.__module__} - {fn.__name__} - {e}")

            return jsonify({"error": str(e)}), 500

    wrapper.__name__ = fn.__name__

    return wrapper


def getaddress(fn):
    """ decorator that logs the route and ip address of visitor

    Args:
        fn (function): [description]
    """

    def wrapper(*args, **kwargs):

        ip_address = request.remote_addr

        route = request.url_rule

        current_app.logger.info(f"Route: {route} | IP Address: {ip_address}")

        return fn(*args, **kwargs)

    wrapper.__name__ = fn.__name__

    return wrapper


def tokenrequired(f):
    """ decorator that checks if access token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("x-access-token")

        # check blacklist
        blacklisted = mongo.db.jwtblacklist.find_one({"Token": token})

        if token != None and token != "" and blacklisted == None:

            try:

                current_user = jwt.decode(
                    token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

                return f(current_user["user"], *args, **kwargs)

            except jwt.ExpiredSignatureError as e:

                return jsonify({"error": "Token Expired"}), 401

            except jwt.DecodeError as e:

                return jsonify({"error": "Token Decode Error"}), 401

        return jsonify({"error": "Token Does Not Exist"}), 401

    decorated.__name__ = f.__name__

    return decorated
