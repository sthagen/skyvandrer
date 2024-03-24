#! /usr/bin/env python
"""Get advanced settings (of ticket management system).

Returns the application properties that are accessible on the Advanced Settings page.
To navigate to the Advanced Settings page in Jira, choose the Jira icon > Jira settings > System, General Configuration and
then click Advanced Settings (in the upper right).

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-jira-settings/#api-rest-api-3-application-properties-advanced-settings-get>

"""

import json
import os

import requests
from requests.auth import HTTPBasicAuth

API_BASE_URL = os.getenv('SUHTEITA_BASE_URL', '')
API_USER = os.getenv('SUHTEITA_USER', '')
API_TOKEN = os.getenv('SUHTEITA_TOKEN', '')

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

url = f'{API_BASE_URL}/rest/api/3/application-properties/advanced-settings'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

response = requests.request('GET', url, headers=headers, auth=auth)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': ')))
