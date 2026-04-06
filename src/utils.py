import unicodedata


def normalizar_texto(texto: str) -> str:
    return (
        unicodedata.normalize("NFKD", texto)
        .encode("ASCII", "ignore")
        .decode("ASCII")
        .lower()
    )


def space():
    print("------------------------------------------------------------------------------")
