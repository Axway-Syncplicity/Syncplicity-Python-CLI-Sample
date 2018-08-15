#!/usr/bin/python3


from API_Caller import CallAPI
import hashlib
import os
import platform
import datetime
import math
import sys
from requests_toolbelt import MultipartEncoder
from FileFolderMetadataClass import FileFolderMetadataClass


class Upload:

    def __init__(self, Credentials, filename='', full_path=''):
        self.AppKey = Credentials.AppKey
        self.AccessToken = Credentials.AccessToken
        self.AsUser = Credentials.AsUser
        self.filename = filename
        self.max_chunk_size = 5242880

        if platform.system() == 'Windows':
            separator = '\\'
        else:
            separator = '/'

        self.full_path = full_path + separator + self.filename
        self.Credentials = Credentials

    def read_in_chunks(self, file_object):
        while True:
            data = file_object.read(self.max_chunk_size)
            if not data:
                break
            yield data

    def creation_date(self):
        if platform.system() == 'Windows':
            return datetime.datetime.fromtimestamp(os.path.getctime(self.full_path)).isoformat()
        else:
            stat = os.stat(self.full_path)
            try:
                return datetime.datetime.fromtimestamp(stat.st_ctime).isoformat()
            except AttributeError:
                return datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()

    def get_url(self, storage_endpoint_id):
        storage_endpoints = FileFolderMetadataClass(self.Credentials).GetStorageEndpoints()
        for storage_endpoint in storage_endpoints:
            if storage_endpoint['Id'] == storage_endpoint_id:
                return storage_endpoint['Urls'][0]['Url']

    def Upload(self, Syncpoint_ID, Path, Storage_Endpoint_ID):
        base_url = self.get_url(Storage_Endpoint_ID)
        url = "saveFile.php?filepath=" + Path
        creation_date = self.creation_date()
        last_write_time = datetime.datetime.fromtimestamp(os.path.getmtime(self.full_path)).isoformat()
        common_headers = {'As-User': '%s' % self.AsUser, "User-Agent": "API_Application"}
        file_size = os.path.getsize(self.full_path)

        if file_size < self.max_chunk_size:
            return self.__upload_file_simple_mode(url, base_url, common_headers, Syncpoint_ID, creation_date, last_write_time)
        else:
            return self.__upload_file_chunked_mode(url, base_url, common_headers, Syncpoint_ID, creation_date, last_write_time, file_size)

    def __upload_file_simple_mode(self, url, base_url, common_headers, Syncpoint_ID, creation_date, last_write_time):
        Method = "POST"
        common_headers["Content-Range"] = "0-*/*"
        multipart_body = [('fileData', ('%s' % self.filename, open('%s' % self.full_path, 'rb'),
                                        'application/octet-stream')),
                            ('sha256', (None, hashlib.sha256(self.full_path.encode('utf-8')).hexdigest(), None)),
                            ('sessionKey', (None, 'Bearer ' + self.AccessToken, None)),
                            ('virtualFolderId', (None, '%s' % Syncpoint_ID, None)),
                            ('creationTimeUtc', (None, creation_date, None)),
                            ('lastWriteTimeUtc', (None, last_write_time, None)),
                            ('fileDone', (None, '', None))]
        return CallAPI(
            url, self.AppKey, self.AccessToken, Method, common_headers, data='',
            file=multipart_body, base_url='%s/' % base_url
        ).MakeRequest()

    def __upload_file_chunked_mode(self, url, base_url, common_headers, Syncpoint_ID, creation_date, last_write_time, file_size):
        initiate_chunked_upload_response = self.__initiate_chunked_upload_session(url, base_url)

        if initiate_chunked_upload_response.status_code != 308:
            sys.exit('Failed to create session for chunked upload')

        common_headers['If-Match'] = initiate_chunked_upload_response.headers['ETag']
        chunk_count = math.ceil(file_size / self.max_chunk_size)

        content_range_index = 0
        sent_chunk_count = 1

        f = open(self.full_path, 'rb')
        for chunk in self.read_in_chunks(f):
            is_last_chunk = sent_chunk_count == chunk_count

            response = self.__upload_file_chunk(
                url, base_url, common_headers, chunk, is_last_chunk, content_range_index,
                Syncpoint_ID, creation_date, last_write_time
            )

            if response.status_code == 308:
                common_headers['If-Match'] = response.headers['ETag']
            else:
                f.close()
                return response

            sent_chunk_count += 1
            content_range_index += self.max_chunk_size

    def __create_chunk_upload_body(self, chunk, is_last_chunk, Syncpoint_ID, creation_date, last_write_time):
        fields = {
            'fileData': (self.filename, chunk, 'application/octet-stream'),
            'sha256': (None, hashlib.sha256(chunk).hexdigest(), None),
            'sessionKey': (None, 'Bearer ' + self.AccessToken, None),
            'virtualFolderId': (None, '%s' % Syncpoint_ID, None),
            'creationTimeUtc': (None, creation_date, None),
            'lastWriteTimeUtc': (None, last_write_time, None)
        }

        if is_last_chunk == True:
            fields['fileDone'] = (None, '', None)

        return MultipartEncoder(fields)

    def __initiate_chunked_upload_session(self, url, base_url):
        Method = "POST"
        initiate_chunked_upload_body = MultipartEncoder({'sessionKey': (None, 'Bearer ' + self.AccessToken, None)})
        initiate_chunked_upload_headers = {
            'As-User': '%s' % self.AsUser,
            "User-Agent": "API_Application",
            'Content-Range': "*/*",
            'Content-Type': initiate_chunked_upload_body.content_type
        }

        return CallAPI(
            url, self.AppKey, self.AccessToken, Method, initiate_chunked_upload_headers,
            data=initiate_chunked_upload_body, base_url='%s/' % base_url
        ).MakeRequest()

    def __upload_file_chunk(self, url, base_url, common_headers, chunk, is_last_chunk, content_range_index, Syncpoint_ID, creation_date, last_write_time):
        Method = "POST"
        common_headers['Content-Range'] = '%s-*/*' % content_range_index
        multipart_body = self.__create_chunk_upload_body(chunk, is_last_chunk, Syncpoint_ID, creation_date, last_write_time)
        common_headers['Content-Type'] = multipart_body.content_type

        return CallAPI(url, self.AppKey, self.AccessToken, Method, common_headers,
                            data=multipart_body, base_url='%s/' % base_url).MakeRequest()