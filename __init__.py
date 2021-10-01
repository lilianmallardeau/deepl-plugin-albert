# -*- coding: utf-8 -*-

"""Deepl plugin for the Albert launcher

This plugin uses the Deepl API to provide translations straight from the Albert Launcher.
Subscribe for the free Deepl API on the Deepl website, and put your API key in the parameters.env file.

Synopsis:
    deepl <target-lang> <text>
    deepl <src-lang:target-lang> <text>"""

from albert import *
import os
import requests
import json
from dotenv import dotenv_values

PARAMETERS = dotenv_values(os.path.dirname(__file__) + '/parameters.env')

__title__ = "Deepl Translator"
__version__ = "0.0.1"
__triggers__ = ["deepl"]
__authors__ = "Lilian MALLARDEAU"
__py_deps__ = ["python-dotenv"]

DEEPL_API_KEY = PARAMETERS['DEEPL_API_KEY']
DEEPL_SUBSCRIPTION = PARAMETERS['DEEPL_SUBSCRIPTION']

DEEPL_API_FREE_BASEURL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_PRO_BASEURL = "https://api.deepl.com/v2/translate"
DEEPL_API_BASEURL = DEEPL_API_PRO_BASEURL if DEEPL_SUBSCRIPTION == "pro" else DEEPL_API_FREE_BASEURL

deepl_icon = os.path.dirname(__file__) + "/DeepL_Logo.svg"


def DeeplItem(*args, **kwargs):
    return Item(*args, icon=deepl_icon, **kwargs)

class DeeplAPIError(Exception):
    def __init__(self, message=""):
        super().__init__()
        self.message = message


def deepl_query(text: str, target_lang: str, source_lang: str=None):
    params = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'target_lang': target_lang
    }
    if source_lang:
        params['source_lang'] = source_lang
    try:
        answer = requests.post(url = DEEPL_API_BASEURL, params = params)
        answer.raise_for_status()
        return answer.json()['translations'][0]
    except:
        try:
            raise DeeplAPIError(answer.json()['message'])
        except KeyError:
            raise DeeplAPIError()


def handleQuery(query):
    if not query.isTriggered:
        return
    
    query_string = query.string.lstrip().rstrip()

    if len(query_string.split(' ')) < 2:
        return showHelp()
    
    try:
        lang = query_string.split(' ')[0]
        text = query_string.lstrip(lang).lstrip().rstrip()
        if lang.count(':') > 1:
            return showHelp()
        [src_lang, target_lang] = lang.split(':') if ':' in lang else [None, lang]
        if "" in (src_lang, target_lang):
            return showHelp()
        answer = deepl_query(text, target_lang, src_lang)
        return DeeplItem(
            id = "deepl_translation",
            text = answer['text'],
            subtext = "Translated from {} to {}".format(answer['detected_source_language'].upper(), target_lang.upper()),
            actions = [
                ClipAction(text="Copy translation to clipboard", clipboardText=answer['text'])
            ]
        )
    except DeeplAPIError as error:
        return DeeplItem(
            id = "deepl_error",
            text = "Deepl API Error",
            subtext = error.message.lstrip('"').rstrip('"')
        )
    except:
        return DeeplItem(
            id = "deepl_error",
            text = "Deepl API Error"
        )


def showHelp():
    return [
        DeeplItem(
            id = "help_1",
            text = "Deepl: detect source language",
            subtext = 'Enter a query in the form "&lt;dest-lang&gt; &lt;text&gt;"'
        ),
        DeeplItem(
            id = "help_2",
            text = "Deepl: specify source language",
            subtext = 'Enter a query in the form "&lt;src-lang:dest-lang&gt; &lt;text&gt;"'
        ),
    ]