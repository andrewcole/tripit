from json import dumps
from os import environ

from illallangi.tripitapi import API, JSONEncoder

access_token = environ["TRIPIT_ACCESS_TOKEN"]
access_token_secret = environ["TRIPIT_ACCESS_TOKEN_SECRET"]
client_token = environ["TRIPIT_CLIENT_TOKEN"]
client_token_secret = environ["TRIPIT_CLIENT_TOKEN_SECRET"]

print(
    dumps(
        API(
            access_token,
            access_token_secret,
            client_token,
            client_token_secret,
            cache=False,
        ),
        cls=JSONEncoder,
        indent=2,
        sort_keys=True,
    )
)
