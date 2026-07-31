from core.extractor import extrair_nf_da_chave, normalizar_numero_nf


def test_extrai_nf_da_chave_48272():
    assert extrair_nf_da_chave("35260749423619000106551000000482721364997117") == "48272"


def test_extrai_nf_da_chave_48252():
    assert extrair_nf_da_chave("35260749423619000106551000000482521104967592") == "48252"


def test_remove_zeros():
    assert normalizar_numero_nf("000048164") == "48164"
