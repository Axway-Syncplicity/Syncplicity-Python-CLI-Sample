# Syncplicity-Python-Sample

Shows examples of various API calls including the initial OAuth2 call.

## Description

This command-line sample application demonstrates various API calls including the initial OAuth2 authentication call.
This type of application would not support SSO-based authentication,
so would be the basis of an application typically used by administrator, not by a regular Syncplicity user.

## System Requirements

* Supported OSs: Windows (tested on Windows10), Linux (tested on Ubuntu)
* Python 3
* Additional Python modules: `requests`, `requests-toolbelt`

### Installation

In order to install modules with Python, you must have PIP (Python's modules installer).
PIP usually comes with Python.
In case you do not have PIP installed, use the link below, it includes instructions for all different OSs:

<https://www.makeuseof.com/tag/install-pip-for-python/>

Once PIP is installed, open a CLI (cmd or shell) and issue the following commands:

    pip install requests
    pip install requests-toolbelt

## Usage

This sample application demonstrates usage of Syncplicity APIs. This is what you need to know or do before you begin to use Syncplicity APIs:

* Make sure you have an Enterprise Edition account you can use to login to the Developer Portal at <https://developer.syncplicity.com>.
* Log into Syncplicity Developer Portal using your Syncplicity login credentials.
  Only Syncplicity Enterprise Edition users are allowed to login to the Developer Portal.
  Based on the configuration done by your Syncplicity administrator,
  Syncplicity Developer Portal will present one of the following options for login:
  * Basic Authentication using Syncplicity username and password.
  * Enterprise Single Sign-on using the web SSO service used by your organization. We support ADFS, OneLogin, Ping and Okta.
* Once you have successfully logged in for the first time,
  you must create an Enterprise Edition sandbox account in the Developer Portal.
  This account can be used to safely test your application using all Syncplicity features
  without affecting your company production data.
  * Log into Syncplicity Developer Portal. Click 'My Profile' and then 'Create sandbox'.
    Refer to the documentation for guidance: <https://developer.syncplicity.com/documentation/overview>.
  * You can log into <https://my.syncplicity.com> using the sandbox account.
    Note that the sandbox account email has "-apidev" suffix.
    So, assuming you regular account email is user@domain.com,
    use user-apidev@domain.com email address to log in to your sandbox account.
* Setup your developer sandbox account:
  * Log into the sandbox account at <https://my.syncplicity.com> to make sure its correctly provisioned and that you can access it.
  * Go to the 'Account' menu.
  * Click "Create" under "Application Token" section.
    The token is used to authenticate an application before making API calls.
    Learn more [here](https://syncplicity.zendesk.com/hc/en-us/articles/115002028926-Getting-Started-with-Syncplicity-APIs).
* Review API documentation by visiting documentation section on the <https://developer.syncplicity.com>.
* Register you application in the Developer Portal to obtain the "App Key" and "App Secret".
  
## Running

### Basic sample

1. Clone the sample project.
2. Use your favorite Python IDE to open the project.
3. Define new application on <https://developer.syncplicity.com>. The app key and app secret values are found in the application page.
  The Syncplicity admin token is found on the "My Account" page of the Syncplicity administration page.
  Use the "Application Token" field on that page to generate a token.
4. Update key values in `ConfigurationFile`:
    * Update the `App Key`
    * Update the `App Secret`
    * Update the `Application Token`
5. Run the application.

### Running On-Behalf-Of sample (As User)

The On Behalf Of sample demonstrates how an administrator can execute actions on behalf of other users (impersonating other users).
Running the On Behalf Of sample requires additional configuration.

You need to specify the GUID of the impersonated user in the `As User` parameter in `ConfigurationFile`.
Examples how the GUID can be retrieved:

* Open the user account page in Syncplicity Administrator Web UI, then the GUID will be in the URL,
  e.g. <https://staging.syncplicity.com/my/Business/EditUser.aspx?userGuid=8f2811ac-b0a7-48ee-b10d-d81649a066d8>.
* Make an API request `GET /provisioning/user.svc/{USER_EMAIL}` and take the `Id` property of the response object.

Besides, the owner of the Application Token must have permissions to execute code on behalf of other users.
By default, Global Administrators do not have this permission. To grant this permission:

1. There must be at least two Global Administrator users in the company.
2. One administrator must sign into Syncplicity (<https://my.syncplicity.com>)
3. Go to the Admin area, User Accounts
4. Find the other administrator account
5. Under "Privileges", click "Modify", select "Access content on behalf of managed users through API" and click "Save"
6. Confirm notification of all administrators about the action

Once this is done, the second administrator account can use the `As User` parameter.

## Team

![alt text][Axwaylogo] Axway Syncplicity Team

[Axwaylogo]: https://github.com/Axway-syncplicity/Assets/raw/master/AxwayLogoSmall.png "Axway logo"

## License

Apache License 2.0
