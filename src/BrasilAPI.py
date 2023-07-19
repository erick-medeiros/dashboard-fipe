import requests
from concurrent.futures import ThreadPoolExecutor
from typing import List

BASE_URL = "https://brasilapi.com.br/api/"


class BrasilAPI:
    debug = False

    def __init__(self, debug: bool = False):
        self.debug = debug

    # url

    def url_fipe_preco(
        self, codigoFipe: str, tabela_referencia: int | None = None
    ) -> str:
        url = BASE_URL + "fipe/preco/v1/{}".format(codigoFipe)
        if tabela_referencia is not None:
            url += "?tabela_referencia=" + str(tabela_referencia)
        return url

    # get

    def get_fipe_marcas(self, tipoVeiculo: str, tabela_referencia: int | None = None):
        url = BASE_URL + "fipe/marcas/v1/{}".format(tipoVeiculo)
        if tabela_referencia is not None:
            url += "?tabela_referencia=" + str(tabela_referencia)
        if self.debug:
            print(url)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_fipe_preco(self, codigoFipe: str, tabela_referencia: int | None = None):
        url = BrasilAPI.url_fipe_preco(self, codigoFipe, tabela_referencia)
        response = requests.get(url)
        if self.debug:
            print(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_fipe_tabelas(self):
        url = BASE_URL + "fipe/tabelas/v1"
        if self.debug:
            print(url)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    # multiples

    def get_multiple_fipe_preco(self, codigoFipe: str, tabela_referencia_list: List[int] | None = None):
        urls = []

        for tabela_referencia in tabela_referencia_list:
            url = BrasilAPI.url_fipe_preco(self, codigoFipe, tabela_referencia)
            urls.append(url)

        def fetch_url(url):
            response = requests.get(url)
            if self.debug:
                print(url)
            return response.json()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(fetch_url, url) for url in urls]
            results = [future.result() for future in futures]

        return results
