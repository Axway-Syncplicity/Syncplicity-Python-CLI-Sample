# encoding = utf-8

import os
import sys
import time
import datetime
import logging
import base64
import json
import requests

# Auth Parameters
CONTENT_TYPE = {'Content-Type': 'application/x-www-form-urlencoded'}
ACCEPT_HEADER = {'Accept': 'application/json'}

NEXT_PAGE_HEADER_NAME = 'X-SYNCP-NEXTPAGE'
CHECKPOINT_NAME_TEMPLATE = 'SYNCP-EVENTS-PLUGIN-8'

TIMESTAMP_NAME = 'timestamp'

def validate_input(helper, definition):
    pass

# Main function
def collect_events(helper, ew):
    
    global CHECKPOINT_NAME_TEMPLATE
    global NEXT_PAGE_HEADER_NAME

    INDEX_NAME = helper.get_output_index()
    CHECKPOINT_NAME = str.format('{}-{}', CHECKPOINT_NAME_TEMPLATE, INDEX_NAME)

    # Get state (dict) from the previous run
    state = helper.get_check_point(CHECKPOINT_NAME)

    # If None - need to fill auth_token to use when call Events API
    if state == None:
        # Get auth token first time
        auth_token = get_auth_token(helper)
        next_page_header = None
        logging.info(auth_token)
        logging.info('State is not found. Read events from the begining.')
    else:
        # Read auth token and next page header from the checkpoint
        auth_token = state.get('auth_token')
        next_page_header = state.get('next_page_header')
        logging.info(str.format('State found. Continue with Next Page Header - {}', next_page_header))

    # Call Events API
    chimera_response = get_chimera_events(helper, auth_token, next_page_header)

    # Validate responce. Expexting: 1) None - when auth failed. 2) List of Events
    chimera_events = validate_chimera_response(chimera_response)

    # Try to renew auth token and repeat request to Events API
    if chimera_events == None:
        logging.info('Failed to get events. Renew auth token and try again.')
        # Renew auth token
        auth_token = get_auth_token(helper)
        # Call Events API
        chimera_response = get_chimera_events(helper, auth_token, next_page_header)
        # Validate responce. Expexting: 1) None - when auth failed. 2) List of Events
        chimera_events = validate_chimera_response(chimera_response)

    # Check that second attempt was successful
    if chimera_events == None:
        chimera_response.raise_for_status()

    # Check that List of Events is not empty to fill NEXT_PAGE_HEADER_NAME with a new value
    if len(chimera_events) > 0:
        next_page_header = chimera_response.headers.get(NEXT_PAGE_HEADER_NAME)

    # Writing events to the splunk
    writh_events(chimera_events, helper, ew)

    # Saving state (dict) from the current run
    state = {'auth_token': auth_token , 'next_page_header': next_page_header}
    helper.save_check_point(CHECKPOINT_NAME, state)

def get_auth_token(helper):

    XML_AUTH_URL = helper.get_arg('token_url')
    auth_headers = get_auth_headers(helper)
    # The following examples send rest requests to some endpoint.
    auth_response = requests.post(XML_AUTH_URL, data={'grant_type': 'client_credentials'}, headers=auth_headers)

    return validate_auth_response(auth_response)

def get_auth_headers(helper):

    global CONTENT_TYPE

    opt_client_id = helper.get_arg('client_id')
    opt_client_secret = helper.get_arg('client_secret')
    opt_app_token = helper.get_arg('app_token')
    base64Encoded = base64.b64encode(str.format('{}:{}', opt_client_id, opt_client_secret))
    auth_headers = {
        'Authorization': str.format('Basic {}', base64Encoded), 
        'Sync-App-Token': opt_app_token }
    auth_headers.update(CONTENT_TYPE)

    return auth_headers

def get_chimera_events(helper, auth_token, next_page_token):

    EVENTS_API_URL = helper.get_arg('events_url')

    opt_limit = helper.get_arg('events_limit')
    auth_headers = get_chimera_auth_headers(helper, auth_token, next_page_token)

    # The following examples send rest requests to some endpoint.
    auth_response = helper.send_http_request(EVENTS_API_URL, 'GET', parameters={'limit': opt_limit}, payload=None,
                                        headers=auth_headers, cookies=None, verify=False, cert=None,
                                        timeout=None, use_proxy=False)
    return auth_response

def get_chimera_auth_headers(helper, auth_token, next_page_header):

    global NEXT_PAGE_HEADER_NAME
    global ACCEPT_HEADER

    auth_headers = {'Authorization': str.format('Bearer {}', auth_token)}
    auth_headers.update(ACCEPT_HEADER)

    if next_page_header != None:
        auth_headers.update({NEXT_PAGE_HEADER_NAME: next_page_header})

    return auth_headers

def validate_auth_response(auth_response):
    # get response status code
    r_status = auth_response.status_code
    if r_status != 200:
        auth_response.raise_for_status()
    
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = auth_response.json()

    return r_json.get('access_token')

def validate_chimera_response(chimera_response):
    # get response status code
    r_status = chimera_response.status_code
    if r_status == 403:
        return None
    elif r_status == 401:
        return None
    elif r_status != 200:
        chimera_response.raise_for_status()
    
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = chimera_response.json()

    return r_json

def writh_events(chimera_events, helper, ew):
    
    global TIMESTAMP_NAME

    INDEX_NAME = helper.get_output_index()
    
    logging.info(str.format('Writing {} events to index {}', len(chimera_events), INDEX_NAME))
    
    for chimera_event in chimera_events:
        json_data = json.dumps(chimera_event)

        event = helper.new_event(
            source=helper.get_input_type(), 
            index=INDEX_NAME,
            sourcetype=helper.get_sourcetype(), 
            time = chimera_event.get(TIMESTAMP_NAME),
            data=json_data)

        ew.write_event(event)
