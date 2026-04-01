
def ranking_pib(df, top_n=10):
    return (
        df.sort_values(by="pib_per_capita", ascending=False)
        .head(top_n)
        [["municipio", "pib_per_capita"]]
        .to_dict(orient="records")
    )


def ranking_idhm(df, top_n=10):
    return (
        df.sort_values(by="idhm", ascending=False)
        .head(top_n)
        [["municipio", "idhm"]]
        .to_dict(orient="records")
    )


def ranking_densidade(df, top_n=10):
    return (
        df.sort_values(by="densidade", ascending=False)
        .head(top_n)
        [["municipio", "densidade"]]
        .to_dict(orient="records")
    )