#!/usr/bin/python3


from API_Caller import CallAPI
from FileFolderMetadataClass import FileFolderMetadataClass


class Download:

    def __init__(self, Credentials, Syncpoint_ID='', file_id=''):
        self.AppKey = Credentials.AppKey
        self.AccessToken = Credentials.AccessToken
        self.AsUser = Credentials.AsUser
        self.vtoken = str(Syncpoint_ID) + "-" + str(file_id)
        self.Credentials = Credentials

    def get_url(self, storage_endpoint_id):
        storage_endpoints = FileFolderMetadataClass(self.Credentials).GetStorageEndpoints()
        for storage_endpoint in storage_endpoints:
            if storage_endpoint['Id'] == storage_endpoint_id:
                return storage_endpoint['Urls'][0]['Url']

    def Download(self, Storage_Endpoint_ID):
        Method = "GET"
        base_url = self.get_url(Storage_Endpoint_ID)
        url = "retrieveFile.php?vToken=%s" % self.vtoken
        headers = { "As-User": self.AsUser }
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, headers, data='',
                          base_url='%s/' % base_url).MakeRequest()

        open('downloaded_file', 'wb').write(request.content)
        
        return request
