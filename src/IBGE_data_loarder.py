import requests
import pandas as pd
from src.utils import space


class IBGEDataLoader:
    BASE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"

    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint: str) -> list:
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            raise RuntimeError(f"Erro ao acessar IBGE: {e}")

    def get_estados(self) -> pd.DataFrame:
        data = self._get("estados")
        return pd.DataFrame(data)

    def get_municipios(self) -> pd.DataFrame:
        data = self._get("municipios")
        return pd.DataFrame(data)

    def get_municipios_por_estado(self, uf: str) -> pd.DataFrame:
        data = self._get(f"estados/{uf}/municipios")
        # df = pd.DataFrame(data)
        # df["municipio"] = df["nome"]
        df = pd.json_normalize(data)

        return df

    def get_municipio_por_id(self, municipio_id: int) -> pd.DataFrame:
        data = self._get(f"municipios/{municipio_id}")
        return pd.DataFrame([data])

