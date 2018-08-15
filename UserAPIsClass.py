#!/usr/bin/python3


import json
from API_Caller import CallAPI


class ClassUserAPIs:

    def __init__(self, Credentials):
        self.AppKey = Credentials.AppKey
        self.AccessToken = Credentials.AccessToken

    def GetAllUsers(self, CompanyID):
        login_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        url = "provisioning/company_users.svc/company/%s/users" % CompanyID
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data='').MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def DeleteUser(self, User):
        login_headers = {'Accept': 'application/json'}
        url = "provisioning/user.svc/%s" % User
        Method = "DELETE"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return request

    def GetUser(self, User):
        login_headers = {'Accept': 'application/json'}
        url = "provisioning/user.svc/%s?include=all_users" % User
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def CreateUser(self,  User, First_Name='', Last_Name='', Password='', Type=7):
        login_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        data = {'EmailAddress': '%s' % User, 'FirstName': '%s' % First_Name, 'LastName': '%s' % Last_Name,
                'Password': '%s' % Password, 'AccountType': Type}
        data = [data]
        json_data = json.dumps(data)
        url = "provisioning/users.svc/?modifier=no_email"
        Method = "POST"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data=json_data).MakeRequest()
        return json.loads(request.content.decode("utf8"))
