# -*- coding: utf-8 -*-

"""
Utility functions to fetch data from web server
"""

import os

import requests
from bs4 import BeautifulSoup
import logger_utils


logger = logger_utils.get_logger(__name__)


class Fetcher():
    """
    facilitates fetching data from webserver
    """

    def __init__(self, target_folder, metadata_source_url, auth=None):
        self.target_folder = target_folder
        self.metadata_source_url = metadata_source_url
        self.auth = auth

        self._ensure_target_folder_exists()

    def _ensure_target_folder_exists(self):
        if not os.path.exists(self.target_folder):
            from distutils.dir_util import mkpath

            mkpath(self.target_folder)

    def fetch(self, name):
        """ fetch file from server """

        logger.info('Fetching {0} from {1}'.format(name, self.metadata_source_url))
        r = requests.get(self.metadata_source_url + '/' + name, stream=True, auth=self.auth)
        with open(self.target_folder + '/' + name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

    def fetch_metadata_from_folder(self):
        """ downloads metadata from archive """

        response = requests.get(self.metadata_source_url, stream=True, auth=self.auth)
        for link in BeautifulSoup(response.content).find_all('a'):
            metadata_filename = link.get('href')
            if metadata_filename.endswith('.xlsx') or metadata_filename.endswith('.txt') or metadata_filename.endswith(
                    '.zip'):
                self.fetch(metadata_filename)