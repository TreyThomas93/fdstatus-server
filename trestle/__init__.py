from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
# from io import BytesIO
# from multipartparser import MultipartParser
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
from flask import current_app
from assets.extensions import mongo

load_dotenv(dotenv_path="config.env")

class Trestle:

    def __init__(self):

        self.mongo = mongo

        self.headers = {
            "User-Agent": "Chrome/95.0.4638.54"
        }

        self.path_to_token = "trestle/token.json"

        self.base_url = "https://api-prod.corelogic.com/trestle/odata"

    def checkAuth(func):
        
        def wrapper(self, *args, **kwargs):

            if not os.path.exists(self.path_to_token):

                obj = self.getNewToken()

                if obj != None:

                    with open(self.path_to_token, "w") as f:

                        self.headers.update(
                            {"Authorization": f"Bearer {obj['access_token']}"})

                        json.dump(obj, f, indent=4)

                return func(self, *args, **kwargs)

            else:

                with open(self.path_to_token, "r") as f:

                    obj = json.load(f)

                    thirty_prior = datetime.fromtimestamp(
                        obj["expires_at"]) - timedelta(minutes=30)

                    if datetime.now() >= thirty_prior:

                        obj = self.getNewToken()

                        with open(self.path_to_token, "w") as f:

                            json.dump(obj, f, indent=4)

                    self.headers.update(
                        {"Authorization": f"Bearer {obj['access_token']}"})

                    return func(self, *args, **kwargs)

        return wrapper

    def getNewToken(self):
        
        c = BackendApplicationClient(client_id=current_app.config["CLIENT_ID"])

        session = OAuth2Session(client=c)

        resp = session.fetch_token(token_url='https://api-prod.corelogic.com/trestle/oidc/connect/token',
                                   client_id=current_app.config["CLIENT_ID"], client_secret=current_app.config["CLIENT_SECRET"],
                                   scope='api')

        return resp

    @checkAuth
    def sendRequest(self, url):

        resp = requests.get(
            url, headers=self.headers, timeout=30)

        return resp