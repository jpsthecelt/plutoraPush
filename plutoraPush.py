#!/usr/bin/python

import sys
import requests
import pprint
import argparse
import json

def createReleaseJson( proto, additional_info, identifier, name, summary, release_type_id, location, release_status,
                       release_risk, impl_date, display_color, organization_id, manager_id, parent_release_id,
                       plutora_release_type, release_project_type):
    return proto

#
# This is a sample program to demonstrate programmatically grabbing JSON
# objects from a file and POSTing them into Plutora
#
def plutoraPush(clientid, clientsecret, plutora_username, plutora_password, object2push):

    # Set up JSON pretty-printing
    pp = pprint.PrettyPrinter(indent=4)

    # Setup for Plutora Get authorization-token (using the 
    # passed parameters, which were obtained from the file 
    # referenced on the command-line
    authTokenUrl = "https://usoauth.plutora.com/oauth/token"
    plutoraBaseUrl = 'https://usapi.plutora.com'
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
        print('plutoraPush.py: Sorry! - [failed on getAuthToken]: ', authResponse.text)
        exit('Sorry, unrecoverable error; gotta go...')
    else:
        accessToken = authResponse.json()["access_token"]
    
        # Experiment -- Get Plutora information for all system releases, or systems, or just the organization-tree
        getReleases = '/releases'
        pushRelease = '/releases'
        getParticularRelease = '/releases/9d18a2dc-b694-4b20-971f-4944420f4038'
        getSystems = '/systems'
        getOrganizationsTree = '/organizations/tree'
        getHosts = '/hosts'
        getSystems = '/systems'
        getOrganizationsTree = '/organizations/tree'

        r = requests.get(plutoraBaseUrl+getReleases, data=payload, headers=headers)
        if r.status_code != 200:
            print('Get release status code: %i' % r.status_code)
            print('\nplutoraPush.py: too bad sucka! - [failed on Plutora get]')
            exit('Sorry, unrecoverable error; gotta go...')
        else:
            releases = r.json
            pp.pprint(r.json())

    try:
        headers["content-type"] = "application/json"
        payload = """{ "additionalInformation": [], "name": "API created System 12", "vendor": "API created vendor", "status": "Active", "organizationId": "%s", "description": "Description of API created System 12" }""" % r.json()['childs'][0]['id']

        r = requests.post(plutoraBaseUrl+pushRelease, data=payload, headers=headers)
        if r.status_code != 201:
            print('Post new workitem status code: %i' % r.status_code)
            print('\nplutoraPush.py: too bad sucka! - [failed on Plutora create system POST]')
            print("header: ", headers)
            pp.pprint(r.json())
            exit('Sorry, unrecoverable error; gotta go...')
        else:
            pp.pprint(r.json())
    except:
        print "EXCEPTION: type: %s, msg: %s " % (sys.exc_info()[0],sys.exc_info()[1].message)
        exit('Error during API processing [POST]')

if __name__ == '__main__':
   # parse commandline and get appropriate passwords
   #    accepted format is python zDeskQuery.py -f <config fiiename> -pusername:password
   #
   parser = argparse.ArgumentParser(description='Get user/password and configuration-filename.')
   parser.add_argument('-c', action='store', dest='config_filename',
                       help='Config filename ')
   parser.add_argument('-p', action='store', dest='proto_filename',
                       help='filename containing JSON object prototype')
   parser.add_argument('-i', action='store', dest='release_id',
                       help='release-id of release to copy')
   results = parser.parse_args()

   config_filename = results.config_filename
   json_filename = results.json_filename

   if len(sys.argv[1:]) < 1:
       parser.usage
       parser.exit()

   if config_filename == None:
       config_filename = 'credentials.cfg'

   # If we don't specify a configfile on the commandline, assume one & try accessing
   # using the specified/assumed configfilename, grab ClientId & Secret from manual setup of Plutora Oauth authorization.
   try:
        with open(config_filename) as data_file:
            data = json.load(data_file)
        client_id = data["credentials"]["clientId"]
        client_secret = data["credentials"]["clientSecret"]
        plutora_username = data["credentials"]["plutoraUser"].replace('@','%40')
        plutora_password = data["credentials"]["plutoraPassword"]
        with open(json_filename) as json_data_file:
            data = json.load(json_data_file)
        json_object = data["postRelease"]
   except:
        # ex.msg is a string that looks like a dictionary
        print "EXCEPTION: type: %s, msg: %s " % (sys.exc_info()[0],sys.exc_info()[1].message)
        exit('couldnt open file {0}'.format(json_filename))

   createReleaseJson(json_object, [], RlsId, RlsName, RlsSummary, RlsTypeId, RlsLocation, RlsStatus,
           RlsRisk, RlsImplDate, RlsDisplayColor, RlsOrgId, RlsMgrId, RlsParentId, RlsType, RlsProjectType)
   plutoraPush(client_id, client_secret, plutora_username, plutora_password, json_object)
