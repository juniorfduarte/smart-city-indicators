from src.utils import normalizar_texto


def test_remove_accents():
    assert normalizar_texto("Maringá") == "maringa"


def test_lowercase():
    assert normalizar_texto("CURITIBA") == "curitiba"


def test_mixed_accents_and_case():
    assert normalizar_texto("São Paulo") == "sao paulo"


def test_no_accents_unchanged():
    assert normalizar_texto("Londrina") == "londrina"


def test_multiple_accents():
    assert normalizar_texto("Pinhão") == "pinhao"
