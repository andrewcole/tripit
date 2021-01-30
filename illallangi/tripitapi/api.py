from functools import cached_property

from click import get_app_dir

from diskcache import Cache

from loguru import logger

from requests import HTTPError, get as http_get

from requests_oauthlib import OAuth1

from yarl import URL

from .tripcollection import TripCollection

ENDPOINTDEF = "https://api.tripit.com/v1"
SUCCESS_EXPIRYDEF = 7 * 24 * 60 * 60
FAILURE_EXPIRYDEF = 0


class API(object):
    def __init__(
        self,
        access_token,
        access_token_secret,
        client_token,
        client_token_secret,
        endpoint=ENDPOINTDEF,
        cache=True,
        config_path=None,
        success_expiry=SUCCESS_EXPIRYDEF,
        failure_expiry=FAILURE_EXPIRYDEF,
        user_agent="tripit-to-sqlite/0.0.1",
        page_size=25,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.auth = OAuth1(
            client_token,
            client_token_secret,
            access_token,
            access_token_secret,
        )
        logger.info(self.auth)
        self.endpoint = URL(endpoint) if not isinstance(endpoint, URL) else endpoint
        self.cache = cache
        self.config_path = get_app_dir(__package__) if not config_path else config_path
        self.success_expiry = success_expiry
        self.failure_expiry = failure_expiry

        self.user_agent = user_agent
        self.page_size = page_size

    @cached_property
    def trips(self):
        return TripCollection(self)

    def get(self, url):
        key = str(url).removeprefix(str(self.endpoint))
        with Cache(self.config_path) as cache:
            if self.cache and key in cache:
                logger.debug(f"Cache Hit on  {key}")
            else:
                logger.debug(f"Cache Miss on {key}, contacting API")
                try:
                    r = http_get(
                        url,
                        headers={"User-Agent": self.user_agent},
                        auth=self.auth,
                    )
                    r.raise_for_status()
                except HTTPError as http_err:
                    logger.error(f"HTTP error occurred: {http_err}")
                    cache.set(key, None, expire=self.failure_expiry)
                    return
                except Exception as err:
                    logger.error(f"Other error occurred: {err}")
                    cache.set(key, None, expire=self.failure_expiry)
                    return
                logger.debug(f"Received {len(r.content)} bytes from API")

                logger.trace(r.request.url)
                logger.trace(r.request.headers)
                logger.trace(r.headers)
                logger.trace(r.text)
                cache.set(key, r.json(), expire=self.success_expiry)
            return cache[key]
