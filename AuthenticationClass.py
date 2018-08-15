#!/usr/bin/python3


import requests
import base64
import json


class Authentication:

    url = 'https://api.syncplicity.com/oauth/token'
    login_data = 'grant_type=client_credentials'

    def __init__(self):
        with open('ConfigurationFile', 'r', newline=None) as Credentials_File:
            self.Credentials = json.load(Credentials_File)
            
        self.AppKey = self.Credentials['App Key']
        self.AppSecret = self.Credentials['App Secret']
        self.AppToken = self.Credentials['Application Token']
        self.AsUser = self.Credentials['As User']

        if self.AppSecret == "":
            raise ValueError('Missing App Secret! Please enter App Secret in configuration file')
        if self.AppToken == "":
            raise ValueError('Missing Application Token! Please enter Application Token in configuration file')

        self.OAuthBasic = base64.b64encode((self.AppKey + ":" + self.AppSecret).encode('ascii')).decode('utf8')
        self.login_headers = {'Authorization': 'Basic %s' % self.OAuthBasic,
                              'Sync-App-Token': '%s' % self.AppToken,
                              'Content-Type': 'application/x-www-form-urlencoded'}

        request = requests.post(self.url, data=self.login_data, headers=self.login_headers)

        if request.status_code != 200:
            raise ValueError(
                'Failed to complete authentication, received error code %s %s' % (request.status_code, request.reason))
                
        json_data = json.loads(request.content.decode('utf8'))
        self.AccessToken = json_data["access_token"]
        self.Company_ID = json_data["user_company_id"]
