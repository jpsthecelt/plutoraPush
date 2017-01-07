#!/usr/bin/python

import requests
import pprint
import argparse
import json

#
# This is a sample program to demonstrate programmatically
# 'grabbing' items from a local JIRA instance and POSTing
# them into Plutora (aka referred to as 'cross-pollinating')
#

def plutoraPush(clientid, clientsecret, plutora_username, plutora_password object2push):

    # Setup for Plutora Get authorization-token (using the 
    # passed parameters, which were obtained from the file 
    # referenced on the command-line
    authTokenUrl = "https://usoauth.plutora.com/oauth/token"
    payload = 'client_id=' + clientid + '&client_secret=' + clientsecret + '&' + 'grant_type=password&username='
    payload = payload + plutora_username + '&password=' + plutora_password + '&='
    
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "bc355474-15d1-1f56-6e35-371b930eac6f"
        }
    
    # Connect to get Plutora access token for subsequent queries
    authResponse = requests.post(authTokenUrl, data=payload, headers=headers)
    if authResponse.status_code != 200:
        print(authResponse.status_code)
        print('pltJiraCrossInteg.py: Sorry! - [failed on getAuthToken]: ', authResponse.text)
        exit('Sorry, unrecoverable error; gotta go...')
    else:
        print('\npltJiraCrossInteg.py - authTokenGet: ')
        pp.pprint(authResponse.json())
        accessToken = authResponse.json()["access_token"]
    
    # Setup to query both JIRA & Maersk Plutora instances
    plutoraMaerskUrl = r'http://maersk.plutora.com/changes/12/comments'
    plutoraMaerskTestUrl = r'https://usapi.plutora.com/me'
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'authorization': "bearer "+accessToken,
        'cache-control': "no-cache",
        'postman-token': "bc355474-15d1-1f56-6e35-371b930eac6f"
    }
    
    # Get Plutora information for a particular release
    plutoraGetReleaseUrl = 'https://usapi.plutora.com/releases/9d18a2dc-b694-4b20-971f-4944420f4038'
    r = requests.get(plutoraGetReleaseUrl, data=payload, headers=headers)
    if r.status_code != 200:
        print r.status_code
        print('\npltJiraCrossInteg.py: too bad sucka! - [failed on JIRA get]')
        exit('Sorry, unrecoverable error; gotta go...')
    else:
        print('\npltJiraCrossInteg.py - Plutora get of release information:')
        pp.pprint(r.json())
    
        # Experiment -- Get Plutora information for all system releases, or systems, or just the organization-tree
        getReleases = '/releases/9d18a2dc-b694-4b20-971f-4944420f4038'
        getSystems = '/systems'
        getOrganizationsTree = '/organizations/tree'
        
        r = requests.get(plutoraBaseUrl+getOrganizationsTree, data=payload, headers=headers)
        if r.status_code != 200:
            print('Get release status code: %i' % r.status_code)
            print('\npltJiraCrossInteg.py: too bad sucka! - [failed on Plutora get]')
            exit('Sorry, unrecoverable error; gotta go...')
        else:
            print('\npltJiraCrossInteg.py - Plutora get of organizations information:')
            pp.pprint(r.json())
    
        getHosts = '/hosts'
        getSystems = '/systems'
        getOrganizationsTree = '/organizations/tree'
    
    # Experiment -- Get Plutora information for all hosts
    #    r = requests.get(plutoraBaseUrl+getHosts, data=payload, headers=headers)
    #    if r.status_code != 200:
    #        print('Get release status code: %i' % r.status_code)
    #        print('\npltJiraCrossInteg.py: too bad sucka! - [failed on Plutora getsystems]')
    #        exit('Sorry, unrecoverable error; gotta go...')
    #    else:
    #        print('\npltJiraCrossInteg.py - Plutora get of systems information:')
    #        pp.pprint(r.json())
    
    # OK; try POSTing something new (workitem, under Release?)
    try:
        headers["content-type"] = "application/json"
        payload = """{ "additionalInformation": [], "name": "API created System 12", "vendor": "API created vendor", "status": "Active", "organizationId": "%s", "description": "Description of API created System 12" }""" % r.json()['childs'][0]['id']

        postWorkitem = '/workitem'
        print("Here's what I'm sending Plutora (headers & payload):")
        print("header: ",headers)
        print("payload: ",payload)
        
        r = requests.post(plutoraBaseUrl+postWorkitem, data=payload, headers=headers)
        if r.status_code != 201:
            print('Post new workitem status code: %i' % r.status_code)
            print('\npltJiraCrossInteg.py: too bad sucka! - [failed on Plutora create system POST]')
            print("header: ",headers)
            pp.pprint(r.json())
            exit('Sorry, unrecoverable error; gotta go...')
        else:
            print('\npltJiraCrossInteg.py - Plutora POST of new workitem information:')
            pp.pprint(r.json())
    except Exception,ex:
        # ex.msg is a string that looks like a dictionary
        print "EXCEPTION: %s " % ex.msg
        exit('Error during API processing [POST]')
        
if __name__ == '__main__':
    try:
        # set up JSON prettyPrinting
        pp = pprint.PrettyPrinter(indent=4)

        # parse commandline and get appropriate passwords
        #    accepted format is python plSuystemCreate.py -f <config fiiename> -pusername:password
        #
        parser = argparse.ArgumentParser(description='Get user/password Plutora and configuration-filename.')
        #   help='JIRA and Plutora logins (username:password)')
        parser.add_argument('-f', action='store', dest='config_filename',
                                help='Config filename ')
        parser.add_argument('-j', action='store', dest='jsonObject',
                            help='Plutora username:password')
        results = parser.parse_args()

        config_filename = results.config_filename.split(':')[0]
        plutora_username = results.jsonObject.split(':')[0].replace('@', '%40')
        plutora_password = results.jsonObject.split(':')[1]

        # If we don't specify a configfile on the commandline, assume one & try accessing
        if len(config_filename) <= 0:
            config_filename = 'credentials.cfg'

        PlutoraUsername = results.jsonObject.split(':')[0].replace('@', '%40')
        PlutoraPassword = results.jsonObject.split(':')[1]

        # using the specified/assumed configfilename, grab ClientId & Secret from manual setup of Plutora Oauth authorization.
        with open(configFilename) as data_file:
            data = json.load(data_file)
        client_id = data["credentials"]["clientId"]
        client_secret = data["credentials"]["clientSecret"]
        plutoraPush(client_id, client_secret, PlutoraUsername, PlutoraPassword, jiraUsername, jiraPassword)

    except Exception,ex:
        # ex.msg is a string that looks like a dictionary
        print "EXCEPTION: %s " % ex.msg
        exit('couldnt open file {0}'.format(config_filename))

    if '__name--' == '__main__'
    print("\n\nWell, it seems we're all done here, boys; time to pack up and go home...")

