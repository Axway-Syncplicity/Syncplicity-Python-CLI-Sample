#!/usr/bin/python3


from API_Caller import CallAPI
import json


class Links:

    def __init__(self, Credentials):
        self.AppKey = Credentials.AppKey
        self.AccessToken = Credentials.AccessToken
        self.AsUser = Credentials.AsUser

    def GetAllLinks(self):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
        url = "syncpoint/links.svc/"
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def CreateLink(self, Syncpoint_ID, VirtualPath, SharedLinkPolicy=3, PasswordPolicy=0,
                   ExpirationPolicy=1, ExpirationDays='2'):
        login_headers = {'As-User': '%s' % self.AsUser,
                         'Accept': 'application/json',
                         "Content-Type": "application/json"}
        url = "syncpoint/links.svc/"
        Method = "POST"
        data = [{"SyncPointId": "%s" % Syncpoint_ID,
                 "VirtualPath": "%s" % VirtualPath,
                 "ShareLinkPolicy": SharedLinkPolicy,
                 "PasswordProtectPolicy": PasswordPolicy,
                 "LinkExpirationPolicy": ExpirationPolicy,
                 "LinkExpireInDays": "%s" % ExpirationDays}]
        json_data = json.dumps(data)
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data=json_data).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def GetLink(self, LinkToken):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
        Method = "GET"
        url = "syncpoint/link.svc/%s" % LinkToken
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def PutLink(self, Syncpoint_ID, LinkToken, Email):
        login_headers = {'As-User': '%s' % self.AsUser,
                         'Accept': 'application/json',
                         "Content-Type": "application/json"}
        Method = "PUT"
        data = {"SyncPointId": "%s" % Syncpoint_ID, 'Users': [{'EmailAddress': '%s' % Email}]}
        json_data = json.dumps(data)
        url = "syncpoint/link.svc/%s?modifier=send_email" % LinkToken
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data=json_data).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def DeleteLink(self, LinkToken):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
        url = "syncpoint/link.svc/%s" % LinkToken
        Method = "DELETE"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return request
