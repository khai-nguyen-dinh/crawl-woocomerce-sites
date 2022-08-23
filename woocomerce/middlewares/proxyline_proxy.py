import requests

from woocomerce.middlewares.base_proxy import BaseProxyMiddleware


class ProxyLineMiddleware(BaseProxyMiddleware):

    def _get_proxies(self):
        with open("proxies.txt", 'r') as data:
            url = f"----"
            response = requests.get(url)
            pl_proxies = response.json()['results']

            proxies = []
            for proxy in pl_proxies:
                line = f'http://{proxy["username"]}:{proxy["password"]}@{proxy["ip"]}:{proxy["port_http"]}'
                proxies.append(line)
            return proxies
