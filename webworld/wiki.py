# -*- coding: utf-8 -*-
"""Module containing functionality to create pages on the MediaWiki"""
import logging
import os

import requests

LOGGER = logging.getLogger(__name__)


def write_page(title, contents, summary="", image_paths=None, wiki_filenames=None):
    if not wiki_filenames:
        wiki_filenames = [os.path.basename(path) for path in image_paths]

    api_url = 'http://173.249.13.4/mediawiki/api.php'
    session = requests.Session()

    _login(api_url, session)
    _edit(api_url, session, title, contents, summary)

    if image_paths:
        _upload(api_url, session, image_paths, wiki_filenames)

    session.close()


def _login(api_url, session):
    username = 'bot'
    password = 'password'  # see https://www.mediawiki.org/wiki/Manual:Bot_passwords

    # get login token
    response_query = session.get(api_url, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
    })
    response_query.raise_for_status()

    # log in
    response_login = session.post(api_url, data={
        'format': 'json',
        'action': 'login',
        'lgname': username,
        'lgpassword': password,
        'lgtoken': response_query.json()['query']['tokens']['logintoken'],
    })
    response_login.raise_for_status()

    if response_login.json()['login']['result'] != 'Success':
        raise RuntimeError(response_login.json()['login']['reason'])


def _edit(api_url, session, title, contents, summary=""):
    # get edit token
    response_query = session.get(api_url, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
    })
    response_query.raise_for_status()

    response_edit = session.post(api_url, data={
        'format': 'json',
        'action': 'edit',
        'assert': 'user',
        'text': contents,
        'summary': summary,
        'title': title,
        'token': response_query.json()['query']['tokens']['csrftoken'],
    })
    response_edit.raise_for_status()

    assert response_edit.json()['edit']['result'] == 'Success'
    LOGGER.info("Wrote page {} to MediaWiki".format(title))


def _upload(api_url, session, paths, wiki_filenames):
    # get edit token
    response_query = session.get(api_url, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
    })
    response_query.raise_for_status()

    for path, wiki_filename in zip(paths, wiki_filenames):
        with open(path, 'rb') as file_to_upload:
            response_upload = session.post(api_url, files=[("file", file_to_upload)], data={
                'format': 'json',
                'action': 'upload',
                'assert': 'user',
                'filename': wiki_filename,
                'ignorewarnings': True,
                'token': response_query.json()['query']['tokens']['csrftoken'],
            })

        response_upload.raise_for_status()

        assert response_upload.json()['upload']['result'] == 'Success'
        LOGGER.info("Uploaded file {} as {}".format(path, wiki_filename))
