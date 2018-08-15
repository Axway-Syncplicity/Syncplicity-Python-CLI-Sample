# Syncplicity-Python-Sample

Shows examples of various API calls including the initial OAuth2 call.

## Description

This command-line sample app demonstrates various API calls including the initial OAuth2 authentication call.
This type of application would not support SSO-based authentication,
so would be the basis of an application typically used by administrator, not by a typical corporate user.

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

* Make sure you have an Enterprise Edition account you can use to login to the <https://developer.syncplicity.com>.
* First time login to Syncplicity:
  * You can log into Syncplicity Developer Portal using your Syncplicity login credentials.
    Only Syncplicity Enterprise Edition users are allowed to login to the Developer Portal.
    Based on the configuration done by your Syncplicity administrator,
    Syncplicity Developer Portal will present one of the following options for login:
    * Basic Authentication using Syncplicity username and password.
    * Enterprise Single Sign-on using the Web-SSO service used by your organization. We support ADFS, OneLogin, Ping and Okta.
* Once you have successfully logged in for the first time,
  the Syncplicity Developer Portal automatically creates an Enterprise Edition sandbox account to help you develop and test your application.
  Here is how it works:
  * The Syncplicity Developer Portal automatically creates your sandbox account
    by appending "-apidev" to the email address you used for logging into the Developer Portal.
    For e.g. if you logged into Syncplicity Developer Portal using user@domain.com as your email address,
    then your associated sandbox account email is user-apidev@domain.com.
  * The Developer Portal will prompt you to set your password for this sandbox account.
  * After you have successfully setup your password,
    you can use the sandbox email address and the newly configured password for logging into your sandbox account
    by visiting <https://my.syncplicity.com> and using "-apidev" email address.
    So, in the example above, you will have to use user-apidev@domain.com email address to log in to your sandbox account.
* Setup your developer sandbox account by configuring your password:
  * Login to your developer sandbox account by visiting <https://my.syncplicity.com> to make sure its correctly provisioned and that you can access it.
  * Through your user profile in the developer sandbox account,
    create an "Application Token" that you will need to authenticate yourself before making API calls.
    Learn more about this [here](https://syncplicity.zendesk.com/hc/en-us/articles/115002028926-Getting-Started-with-Syncplicity-APIs).
  * Review API documentation by visiting Docs page on the <https://developer.syncplicity.com>.
  * Register you app in the Developer Portal to obtain the "App Key" and "App Secret".
  
## Running

### Basic sample

1. Clone the sample project.
2. Use your favorite Python IDE to open the project.
3. Define new app on <https://developer.syncplicity.com>. The app key and app secret values are found in the application page.
  The Syncplicity admin token is found on the "My Account" page of the Syncplicity administration page.
  Use the "Application Token" field on that page to generate a token.
4. Update key values in `ConfigurationFile`:
    * Update the App Key
    * Update the App Secret
    * Update the Application Token
    * In case you would like to run this app on behalf of a user, enter the GUID to As User
5. Run the application.

## Team

![alt text][Axwaylogo] Axway Syncplicity Team

[Axwaylogo]: https://github.com/Axway-syncplicity/Assets/raw/master/AxwayLogoSmall.png "Axway logo"

## License

Apache License 2.0
