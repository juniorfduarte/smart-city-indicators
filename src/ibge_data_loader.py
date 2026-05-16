import logging

import pandas as pd
import requests

logger = logging.getLogger(__name__)


class IBGEDataLoader:
    BASE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"

    def __init__(self) -> None:
        self.session = requests.Session()

    def _get(self, endpoint: str) -> list:
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Erro ao acessar IBGE API: %s", e)
            raise RuntimeError(f"Erro ao acessar IBGE: {e}") from e

    def get_estados(self) -> pd.DataFrame:
        return pd.DataFrame(self._get("estados"))

    def get_municipios(self) -> pd.DataFrame:
        return pd.DataFrame(self._get("municipios"))

    def get_municipios_por_estado(self, uf: str) -> pd.DataFrame:
        return pd.json_normalize(self._get(f"estados/{uf}/municipios"))

    def get_municipio_por_id(self, municipio_id: int) -> pd.DataFrame:
        return pd.DataFrame([self._get(f"municipios/{municipio_id}")])
