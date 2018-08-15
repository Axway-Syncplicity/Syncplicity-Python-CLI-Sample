#!/usr/bin/python3


import json
from API_Caller import CallAPI


class Groups:

    def __init__(self, Credentials):
            self.AppKey = Credentials.AppKey
            self.AccessToken = Credentials.AccessToken

    def GetAllGroups(self, CompanyID):
        login_headers = {'Accept': 'application/json'}
        url = "provisioning/groups.svc/%s/groups" % CompanyID
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data='').MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def GetGroupMembers(self, GroupID):
        login_headers = {'Accept': 'application/json'}
        url = "provisioning/group_members.svc/%s" % GroupID
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def GetUserGroups(self, UserID):
        login_headers = {'Accept': 'application/json'}
        url = "provisioning/user_groups.svc/user/%s/groups" % UserID
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def DeleteGroup(self, GroupID):
        login_headers = {}
        url = "provisioning/group.svc/%s" % GroupID
        Method = "DELETE"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return request

    def GetGroupMember(self, User, GroupID):
        login_headers = {'Accept': 'application/json'}
        url = "provisioning/group_member.svc/%s/member/%s" % (GroupID, User)
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def DeleteUserFromGroup(self, User, GroupID):
        login_headers = {}
        url = "provisioning/group_member.svc/%s/member/%s" % (GroupID, User)
        Method = "DELETE"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return request

    def AddUserToGroup(self, User, GroupID):
        login_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        data = [{'EmailAddress': '%s' % User}]
        json_data = json.dumps(data)
        url = "provisioning/group_members.svc/%s" % GroupID
        Method = "POST"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data=json_data).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def CreateGroup(self, GroupName, OwnerEmail, CompanyID):
        login_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        url = "provisioning/groups.svc/%s/groups" % CompanyID
        data = [{"Name": '%s' % GroupName, "Owner": {"EmailAddress": '%s' % OwnerEmail}}]
        json_data = json.dumps(data)
        Method = "POST"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data=json_data).MakeRequest()
        return json.loads(request.content.decode("utf8"))
