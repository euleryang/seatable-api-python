import json
import requests


def parse_headers(token):
    return {
        'Authorization': 'Token ' + token,
        'Content-Type': 'application/json',
    }


def parse_server_url(server_url):
    return server_url.rstrip('/')


def parse_response(response):
    if response.status_code >= 400:
        raise ConnectionError(response.status_code, response.content)
    else:
        data = json.loads(response.content)
        return data


class SeaTableAPI(object):
    """SeaTable API
    """

    def __init__(self, token, server_url):
        """
        :param token: str
        :param server_url: str
        """
        self.token = token
        self.server_url = parse_server_url(server_url)
        self.dtable_server_url = None
        self.uuid = None
        self.headers = None

    def __str__(self):
        return 'SeaTableAPI Object [ %s ]' % self.uuid

    def auth(self):
        """Auth to SeaTable
        """
        url = self.server_url + '/api/v2.1/dtable/app-access-token/'
        headers = parse_headers(self.token)
        response = requests.get(url, headers=headers)
        data = parse_response(response)

        self.uuid = data.get('dtable_uuid')
        jwt_token = data.get('access_token')
        self.headers = parse_headers(jwt_token)
        self.dtable_server_url = parse_server_url(data.get('dtable_server'))

    def _row_server_url(self):
        return self.dtable_server_url + '/api/v1/dtables/' + self.uuid + '/rows/'

    def list_rows(self, table_name, view_name=None):
        """
        :param table_name: str
        :param view_name: str
        :return: list
        """
        url = self._row_server_url()
        params = {
            'table_name': table_name,
        }
        if view_name:
            params['view_name'] = view_name
        response = requests.get(url, params=params, headers=self.headers)
        data = parse_response(response)
        return data.get('rows')

    def append_row(self, table_name, row_data):
        """
        :param table_name: str
        :param row_data: dict
        """
        url = self._row_server_url()
        json_data = {
            'table_name': table_name,
            'row': row_data,
        }
        response = requests.post(url, json=json_data, headers=self.headers)
        return parse_response(response)

    def insert_row(self, table_name, row_data, anchor_row_id):
        """
        :param table_name: str
        :param row_data: dict
        :param anchor_row_id: str
        """
        url = self._row_server_url()
        json_data = {
            'table_name': table_name,
            'row': row_data,
            'anchor_row_id': anchor_row_id,
        }
        response = requests.post(url, json=json_data, headers=self.headers)
        return parse_response(response)

    def update_row(self, table_name, row_id, row_data):
        """
        :param table_name: str
        :param row_id: str
        :param row_data: dict
        """
        url = self._row_server_url()
        json_data = {
            'table_name': table_name,
            'row_id': row_id,
            'row': row_data,
        }
        response = requests.put(url, json=json_data, headers=self.headers)
        return parse_response(response)

    def delete_row(self, table_name, row_id):
        """
        :param table_name: str
        :param row_id: str
        """
        url = self._row_server_url()
        json_data = {
            'table_name': table_name,
            'row_id': row_id,
        }
        response = requests.delete(url, json=json_data, headers=self.headers)
        return parse_response(response)
