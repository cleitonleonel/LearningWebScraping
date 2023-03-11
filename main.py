"""Arquivo base para o desenvolvimento de apps e automação de determinados sites,
tendo como base a classe Browser, aqui serão criados as chamadas de apis
para esses sites.
"""
from apps import (
    eurowin
)


def start_eurowin():
    """Inicia a API do Eurowin e faz a autenticação com as credenciais fornecidas."""
    api = eurowin.Api(
        "user@gmail.com",
        "password"
    )
    print(api.auth())


if __name__ == "__main__":
    start_eurowin()
