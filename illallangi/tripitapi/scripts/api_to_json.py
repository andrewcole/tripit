from json import dump

from click import (
    File as FILE,
    STRING,
    argument,
    command,
    option,
)

from illallangi.tripitapi import API, JSONEncoder


@command()
@option(
    "--access-token",
    envvar="TRIPIT_ACCESS_TOKEN",
    help="Tripit OAuth access token",
    required=True,
    type=STRING,
)
@option(
    "--access-token-secret",
    envvar="TRIPIT_ACCESS_TOKEN_SECRET",
    help="Tripit OAuth access token secret",
    required=True,
    type=STRING,
)
@option(
    "--client-token",
    envvar="TRIPIT_CLIENT_TOKEN",
    help="Tripit OAuth client token",
    required=True,
    type=STRING,
)
@option(
    "--client-token-secret",
    envvar="TRIPIT_CLIENT_TOKEN_SECRET",
    help="Tripit OAuth client token secret",
    required=True,
    type=STRING,
)
@option("--output", default="-", help="File to write to", type=FILE("w", atomic=True))
def cli(access_token, access_token_secret, client_token, client_token_secret, output):
    dump(
       {
            'access_token': access_token,
            'access_token_secret': access_token_secret,
            'client_token': client_token,
            'client_token_secret': client_token_secret,
        },    
        output,
        cls=JSONEncoder,
        indent=2,
        sort_keys=True,
    )


if __name__ == "__main__":
    cli()
