# -*- coding: utf-8 -*-
'''
Utility functions to fetch data from web server
'''

import os
import sys
import glob
import requests
from bs4 import BeautifulSoup
from distutils.dir_util import mkpath
import logger_utils

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

logger = logger_utils.get_logger(__name__)

project_name_passwd_map = {
    'melanoma': 'BPA_MELANOMA_DOWNLOADS_PASSWORD',
    'base': 'BPA_BASE_DOWNLOADS_PASSWORD',
    'users': 'BPA_USERS_DOWNLOADS_PASSWORD',
    'gbr': 'BPA_GBR_DOWNLOADS_PASSWORD',
    'sepsis': 'BPA_SEPSIS_DOWNLOADS_PASSWORD',
    'marine': 'BPA_MM_DOWNLOADS_PASSWORD',
}


def get_password(project_name=None):
    '''Get downloads password for project from environment '''

    def complain_and_quit():
        logger.error('Please set shell variable {} to current BPA {} project password'.format(password_env,
                                                                                              project_name))
        sys.exit()

    password_env = project_name_passwd_map.get(project_name, None)
    if password_env is None:
        logger.error('Set project_name')
        sys.exit()

    if password_env not in os.environ:
        complain_and_quit()

    password = os.environ[password_env]
    if password == '':
        complain_and_quit()

    return password


class Fetcher():
    ''' facilitates fetching data from webserver '''

    def __init__(self, target_folder, metadata_source_url, auth=None):
        self.target_folder = target_folder
        self.metadata_source_url = metadata_source_url
        self.auth = auth
        self.filename_url = {}

        self._ensure_target_folder_exists()

    def _ensure_target_folder_exists(self):
        if not os.path.exists(self.target_folder):

            mkpath(self.target_folder)

    def clean(self):
        ''' Clean up existing contents '''

        files = glob.glob(self.target_folder + '/*')
        for f in files:
            os.remove(f)

    def fetch(self, name):
        ''' fetch file from server '''

        logger.info('Fetching {0} from {1}'.format(name, self.metadata_source_url))
        url = self.metadata_source_url + '/' + name
        self.filename_url[name] = url
        r = requests.get(url, stream=True, auth=self.auth, verify=False)
        with open(self.target_folder + '/' + name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

    def fetch_metadata_from_folder(self, fetch_gz=False):
        ''' downloads metadata from archive '''

        logger.info('Fetching folder from {}'.format(self.metadata_source_url))
        response = requests.get(self.metadata_source_url, stream=True, auth=self.auth, verify=False)
        downloaded = set()
        for link in BeautifulSoup(response.content, 'html.parser').find_all('a'):
            metadata_filename = link.get('href')
            if metadata_filename in downloaded:
                continue
            if metadata_filename.endswith('.xlsx') or \
                    metadata_filename.endswith('.txt') or \
                    metadata_filename.endswith('.csv') or \
                    metadata_filename.endswith('.md5'):
                self.fetch(metadata_filename)
                downloaded.add(metadata_filename)

            if fetch_gz is True and metadata_filename.endswith('.gz'):
                self.fetch(metadata_filename)
