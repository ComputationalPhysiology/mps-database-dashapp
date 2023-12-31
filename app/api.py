import logging
import requests
import json

logger = logging.getLogger(__name__)


class Api:
    def __init__(self, username, password, baseurl, timeout=15) -> None:
        logger.info("Create api instance")

        error_messages = []
        if username is None:
            error_messages.append("No username provided. Please the the environment variable 'MPS_DATABASE_USERNAME'")

        if password is None:
            error_messages.append("No password provided. Please the the environment variable 'MPS_DATABASE_PASSWORD'")

        if baseurl is None:
            error_messages.append("No base url provided. Please the the environment variable 'MPS_DATABASE_BASEURL'")

        self._username = username
        self._password = password
        self._baseurl = baseurl
        self._timeout = timeout

        if error_messages:
            msg = "\n".join(error_messages)
            raise ValueError(msg)

        try:
            self._get_access_token()
        except requests.exceptions.ConnectTimeout:
            self._auth = None

    def _get_access_token(self):
        response = requests.post(
            f"{self._baseurl}/auth/login",
            {"username": self._username, "password": self._password},
            timeout=self._timeout,
        )

        self._auth = response.json()

    def _get(self, url):
        logger.info(f"Get {url}")
        response = requests.get(url, headers=self.access_headers, timeout=self._timeout)

        if response.status_code == 401:
            self._get_access_token()
            response = requests.get(url, headers=self.access_headers, timeout=self._timeout)

        if not response.status_code == 200:
            msg = f"Failed to get url {url}: {response.text}"
            logger.warning(msg)
            return msg
        return json.loads(response.content)

    def _post(self, url, data):
        logger.info(f"Post {url}: {data}")
        response = requests.post(url, json=data, headers=self.access_headers, timeout=self._timeout)
        if response.status_code == 401:
            self._get_access_token()
            response = requests.post(url, json=data, headers=self.access_headers, timeout=self._timeout)

        if not response.status_code == 200:
            msg = f"Request to url {url} failed with data {data}: " f"{response.text}"
            logger.warning(msg)
            return msg
        return json.loads(response.content)

    @property
    def access_headers(self):
        if self._auth is None:
            msg = "Api is not connected to the server"
            raise RuntimeError(msg)
        token = self._auth["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def users(self):
        return self._get(f"{self._baseurl}/users")

    def list_drugs(self):
        return self._get(f"{self._baseurl}/drug")

    def list_cell_lines(self):
        return self._get(f"{self._baseurl}/cell_line")

    def list_experiments(self):
        return self._get(f"{self._baseurl}/experiment")

    def search(self, data):
        return self._post(f"{self._baseurl}/mps_data/search", data)

    def analysis_settings(self, mps_data_id):
        return self._get(
            f"{self._baseurl}/mps_data/analyse_settings/{mps_data_id}",
        )

    def mps_data(self, mps_data_id):
        return self._get(
            f"{self._baseurl}/mps_data/{mps_data_id}",
        )

    def tissue_detection(self, mps_data_id, mask_sigma, method, template_name, transpose_template):
        return self._get(
            f"{self._baseurl}/mps_data/tissue-detection/{mps_data_id}?mask_sigma={mask_sigma}&method={method}&template_name={template_name}&transpose_template={transpose_template}",
        )

    def mps_data_by_experiment(self, experiment_name):
        return self._get(
            f"{self._baseurl}/mps_data/experiment/{experiment_name}",
        )

    def mps_data_detailed_info(self, ids: list[int]):
        return self._post(f"{self._baseurl}/mps_data/detailed_info", {"ids": ids})
