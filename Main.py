#!/usr/bin/python3

from UserAPIsClass import ClassUserAPIs
from AuthenticationClass import Authentication
from FileFolderMetadataClass import FileFolderMetadataClass
import json
from UploadFileClass import Upload
from DownloadFileClass import Download
from LinksAPIsClass import Links
from GroupAPIsClass import Groups
import datetime
import time
import sys
import os


Credentials = Authentication()
CompanyID = Credentials.Company_ID

# call class
Content = FileFolderMetadataClass(Credentials)

# get storage endpoints
Storage_Endpoints = Content.GetStorageEndpoints()
print('Getting storage endpoints...\n' + json.dumps(Storage_Endpoints, sort_keys=True, indent=4) + '\n')

# get all syncpoints
All_Syncpoints = Content.GetAllSyncpoints()
print('Getting syncpoints...\n' + json.dumps(All_Syncpoints, sort_keys=True, indent=4) + '\n')

# create syncpoint
print('Creating syncpoint...\n')
Syncpoint = Content.CreateSyncpoint(Syncpoint_Name='TestPoint')
print(json.dumps(Syncpoint, sort_keys=True, indent=4) + '\n')

# create folder in syncpoint
print('Creating folder in syncpoint...\n')
Folder = Content.CreateFolderSP(Syncpoint=Syncpoint[0]['Id'], NewFolder='TestFolder')
print(json.dumps(Folder, sort_keys=True, indent=4) + '\n')

# get folder from syncpoint
print('Getting new folder...\n' + json.dumps(Content.GetFolderFromSyncpoint(Syncpoint[0]['Id'],
                                             Folder[0]['FolderId']), sort_keys=True, indent=4) + '\n')

# upload file
print('Uploading file...\n')
Filename = 'TestFile'
Path = '%5C' + '%s' % Folder[0]['Name'] + '%5C' + "%s" % Filename
Storage_Endpoint_ID = Syncpoint[0]['StorageEndpointId']
Full_Path = os.getcwd().encode().decode()
UploadFile = Upload(Credentials, filename='%s' % Filename, full_path=Full_Path).Upload(Syncpoint[0]['Id'], Path,
                                                                                       Storage_Endpoint_ID)
print(UploadFile.content.decode("utf8"))

# get file
time.sleep(5)  # 5 seconds delay since file was just uploaded
print('Getting file...\n')
Get_File = Content.GetFilesFromFolder(Syncpoint[0]['Id'], Folder[0]['FolderId'])
if not Get_File:
    Get_File = Content.GetFilesFromFolder(Syncpoint[0]['Id'], Folder[0]['FolderId'])
    if not Get_File:
        print('Failed to get file')
        sys.exit()
else:
    print(json.dumps(Get_File, sort_keys=True, indent=4) + '\n')

# download file
print('Downloading file and saving as downloaded_file...\n')
Download(Credentials, Syncpoint_ID=Syncpoint[0]['Id'], file_id=Get_File[0]['LatestVersionId']).\
    Download(Storage_Endpoint_ID)

# create shared link
print('Creating shared link...\n')
Initiate_Link = Links(Credentials)
VirtualPath = '\\' + Folder[0]['Name'] + '\\' + Filename
Link = Initiate_Link.CreateLink(Syncpoint_ID=Syncpoint[0]['Id'], VirtualPath=VirtualPath)
print(json.dumps(Link, sort_keys=True, indent=4) + '\n')

# get link
print('Getting link...\n')
GetLink = Initiate_Link.GetLink(Link[0]['Token'])
print(json.dumps(GetLink, sort_keys=True, indent=4) + '\n')

# put link
print('Putting link...\n')
PutLink = Initiate_Link.PutLink(Syncpoint[0]['Id'], Link[0]['Token'], Email='aharari@axway.com')
print(json.dumps(PutLink, sort_keys=True, indent=4) + '\n')

# delete link
print('Deleting link...\n')
DeleteLink = Initiate_Link.DeleteLink(Link[0]['Token'])
if DeleteLink.status_code == 200:
    print('Link was deleted successfully\n')
else:
    print('Failed to delete link')

# delete file
print('Deleting file...\n')
DeleteFile = Content.DeleteFile(Syncpoint[0]['Id'], Get_File[0]['LatestVersionId'])
if DeleteFile.status_code == 200:
    print('File was deleted successfully\n')
else:
    print('Failed to delete file\n')

# delete folder
print('Deleting folder...\n')
DeleteFolder = Content.DeleteFolder(Syncpoint[0]['Id'], Folder[0]['FolderId'])
if DeleteFolder.status_code == 200:
    print('Folder was deleted successfully\n')
else:
    print('Failed to delete folder\n')

# delete syncpoint
print('Deleting syncpoint...\n')
DeleteSyncpoint = Content.DeleteSyncpoint(Syncpoint[0]['Id'])
if DeleteSyncpoint.status_code == 200:
    print('Syncpoint was deleted successfully\n')
else:
    print('Failed to delete syncpoint\n')

print('Provisioning user\n')

# initiate class
Provisioning = ClassUserAPIs(Credentials)

# create user
print('Creating user...\n')
User = Provisioning.CreateUser(User='fakeuser-%s@fakedomain.com' % datetime.datetime.now().microsecond,
                               First_Name='fake', Last_Name='user', Password='Aa!2345678')
print(json.dumps(User, sort_keys=True, indent=4) + '\n')

# create group
print('Creating group...\n')
InitiateGroup = Groups(Credentials)
Group = InitiateGroup.CreateGroup(GroupName='NewTestGroup', OwnerEmail=User[0]['EmailAddress'], CompanyID=CompanyID)
print(json.dumps(Group, sort_keys=True, indent=4) + '\n')

# add user to group
print('Adding user to group...\n')
UserToGroup = InitiateGroup.AddUserToGroup(User[0]['EmailAddress'], Group[0]['Id'])
print(json.dumps(UserToGroup, sort_keys=True, indent=4) + '\n')

# remove user from group
print('Removing user from group...\n')
RemoveFromGroup = InitiateGroup.DeleteUserFromGroup(User[0]['EmailAddress'], Group[0]['Id'])
if RemoveFromGroup.status_code == 200:
    print('User successfully removed from group\n')
else:
    print('Failed to remove user from group\n')

# delete group
print("Deleting group...\n")
DeleteGroup = InitiateGroup.DeleteGroup(Group[0]['Id'])
if DeleteGroup.status_code == 200:
    print('Deleted group successfully\n')
else:
    print("Failed to delete group\n")

# delete user
print("Deleting user...\n")
DeleteUser = Provisioning.DeleteUser(User[0]['EmailAddress'])
if DeleteUser.status_code == 200:
        print('Deleted user successfully\n')
else:
    print("Failed to delete user\n")
