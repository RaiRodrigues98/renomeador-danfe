import pytest

from core.leitor_nf import localizar_numero


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("NF-e Nº 000012345 SÉRIE 1", "12345"),
        ("NF-e No. 000048272 Série 100", "48272"),
        ("NOTA FISCAL ELETRÔNICA N° 987654 Série 001", "987654"),
        ("Nº 45678 SÉRIE 2 FOLHA 1/1", "45678"),
        ("123456 FOLHA 1/1", "123456"),
    ],
)
def test_localizar_numero(texto, esperado):
    assert localizar_numero(texto) == esperado


def test_nao_confunde_chave_de_acesso():
    texto = "CHAVE DE ACESSO 35260712345678000123550010000098761000098765"
    assert localizar_numero(texto) is None
