#!/usr/bin/python3


import json
from API_Caller import CallAPI


class FileFolderMetadataClass:

    def __init__(self, Credentials):
        self.AppKey = Credentials.AppKey
        self.AccessToken = Credentials.AccessToken
        self.AsUser = Credentials.AsUser

    def GetStorageEndpoints(self):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
        url = "storage/storageendpoints.svc/"
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        if request.status_code == 200:
            return json.loads(request.content.decode("utf8"))
        else:
            print('Failed to get storage endpoints')

    def GetDefaultStorage(self):
            login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
            url = "storage/storageendpoint.svc/"
            Method = "GET"
            request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
            if request.status_code == 200:
                return json.loads(request.content.decode("utf8"))
            else:
                print('Failed to get default storage')

    def GetAllSyncpoints(self):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
        url = "syncpoint/syncpoints.svc/?includeType=1,2,3,4,5,6,7,8"
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        if request.status_code == 200:
            return json.loads(request.content.decode("utf8"))
        else:
            print('Failed to get syncpoints')

    def CreateSyncpoint(self, Syncpoint_Name):
            login_headers = {'As-User': '%s' % self.AsUser,
                             'Accept': 'application/json',
                             'Content-Type': 'application/json'}
            data = [{"Type": 6,
                     "Name": "%s" % Syncpoint_Name,
                     "Mapped": 0,
                     "DownloadEnabled": 0,
                     "UploadEnabled": 0,
                     "StorageEndpointID": "%s" % self.GetDefaultStorage()['Id']}]
            json_data = json.dumps(data)
            url = "syncpoint/syncpoints.svc/"
            Method = "POST"
            request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data=json_data).MakeRequest()
            return json.loads(request.content.decode("utf8"))

    def CreateFolderSP(self, Syncpoint, NewFolder):
        login_headers = {'As-User': '%s' % self.AsUser,
                         'Accept': 'application/json',
                         'Content-Type': 'application/json'}
        data = [{"SyncpointId": "%s" % Syncpoint,
                 "Name": "%s" % NewFolder,
                 "Status": 1,
                 "VirtualPath": "\\%s" % NewFolder}]
        Method = "POST"
        json_data = json.dumps(data)
        url = "sync/folders.svc/%s/folders" % Syncpoint
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data=json_data).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def CreateFolder(self, SyncpointID, FolderID, NewFolder):
        login_headers = {'As-User': '%s' % self.AsUser,
                         'Accept': 'application/json',
                         'Content-Type': 'application/json'}
        data = [{"Name": "%s" % NewFolder, "Status": 1}]
        json_data = json.dumps(data)
        url = "sync/folder_folders.svc/%s/folder/%s/folders" % (SyncpointID, FolderID)
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data=json_data).MakeRequest()
        print(json.dumps(json.loads(request.content.decode("utf8")), sort_keys=True, indent=4))

    def GetFolderFromSyncpoint(self, Syncpoint, FolderID):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
        url = "sync/folder.svc/%s/folder/%s?include=active" % (Syncpoint, FolderID)
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data='').MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def GetFileFromSyncpoint(self, Syncpoint_ID, File_ID):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
        url = "sync/file.svc/%s/file/%s" % (Syncpoint_ID, File_ID)
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def GetFilesFromFolder(self, Syncpoint_ID, Folder_ID):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
        url = "sync/folder_files.svc/%s/folder/%s/files" % (Syncpoint_ID, Folder_ID)
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def GetFoldersFromSyncpoint(self, SyncpointID):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
        url = "sync/folders.svc/%s/folders" % SyncpointID
        Method = "GET"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return json.loads(request.content.decode("utf8"))

    def DeleteFolder(self, Syncpoint_ID, Folder_ID):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json'}
        url = "sync/folder.svc/%s/folder/%s" % (Syncpoint_ID, Folder_ID)
        Method = "DELETE"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return request

    def DeleteSyncpoint(self, Syncpoint_ID):
        login_headers = {'As-User': '%s' % self.AsUser, 'Accept': 'application/json', 'Content-Type': ''}
        url = "syncpoint/syncpoint.svc/%s" % Syncpoint_ID
        Method = "DELETE"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return request

    def DeleteFile(self, SyncpointID, FileID):
        login_headers = {'Accept': 'application/json'}
        url = "sync/file.svc/%s/file/%s" % (SyncpointID, FileID)
        Method = "DELETE"
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers).MakeRequest()
        return request
