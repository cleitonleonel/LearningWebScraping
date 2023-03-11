import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)


class Browser:
    """
    Uma classe que fornece funcionalidade para enviar requisições HTTP e analisar a resposta com BeautifulSoup.

    Atributos:
    -----------
    response: requests.Response
        O objeto de resposta obtido após o envio de uma requisição.
    headers: dict
        Os cabeçalhos a serem enviados com a requisição.
    session: requests.Session
        O objeto de sessão usado para enviar as requisições.

    Métodos:
    --------
    get_headers() -> dict:
        Retorna os cabeçalhos a serem enviados com a requisição.
    get_soup() -> BeautifulSoup:
        Analisa o conteúdo da resposta usando BeautifulSoup e retorna um objeto BeautifulSoup.
    send_request(method: str, url: str, **kwargs) -> requests.Response:
        Envia uma requisição HTTP usando o método e URL fornecidos, juntamente com quaisquer argumentos adicionais.

    """

    def __init__(self):
        self.response = None
        self.headers = self.get_headers()
        self.session = requests.Session()

    def get_headers(self) -> dict:
        """
        Retorna os cabeçalhos a serem enviados com a requisição.

        Retorna:
        --------
        dict
            Os cabeçalhos a serem enviados com a requisição.
        """
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36"
        }
        return self.headers

    def get_soup(self) -> BeautifulSoup:
        """
        Analisa o conteúdo da resposta usando BeautifulSoup e retorna um objeto BeautifulSoup.

        Retorna:
        --------
        BeautifulSoup
            O conteúdo analisado da resposta como um objeto BeautifulSoup.
        """
        return BeautifulSoup(self.response.content, "html.parser")

    def send_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Envia uma requisição HTTP usando o método e URL fornecidos, juntamente com quaisquer argumentos adicionais.

        Parâmetros:
        -----------
        method: str
            O método HTTP a ser usado para a requisição.
        url: str
            A URL para a qual a requisição será enviada.
        **kwargs:
            Quaisquer argumentos de palavra-chave adicionais a serem passados para requests.Session.request().

        Retorna:
        --------
        requests.Response
            O objeto de resposta obtido após o envio da requisição.
        """
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504, 104],
            allowed_methods=["HEAD", "POST", "PUT", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        try:
            self.response = self.session.request(method, url, **kwargs)
            self.response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Ocorreu um erro ao enviar a requisição: {e}")
        return self.response
