#!/usr/local/bin/python3

import sys
import os
import requests
import json
import time

LOGGER=False #must be off when called via terraform - set to True when debugging this script manually

WAIT_AFTER_CREATE=5         # seconds to wait after creating an app before trying to get its ID
WAIT_BETWEEN_RETRIES=10     # number of seconds to wait between attempts to grab the ID
RETRIES=10                  # total numberof attempts to get ID before erroring out


# Check we have the information we need
if(len(sys.argv) < 4):
    sys.stderr.write("App name and api key and app type must be supplied as arguments\n")
    exit(1)

if(not(os.environ.get('NEWRELIC_API_KEY'))):
    print('NEWRELIC_API_KEY not present')
    sys.stderr.write("NEWRELIC_API_KEY not present\n")
    exit(1)


APP_NAME=sys.argv[1]
APP_API_KEY=sys.argv[2]
APP_TYPE=sys.argv[3]
WORKING_DIRECTORY=os.path.dirname(os.path.abspath(__file__))

if(not(APP_TYPE=="node" or APP_TYPE=="java")):
    sys.stderr.write("Only node and java app types are supported\n")
    exit(1)


def logger(log):
    if(LOGGER):
        print(log)

def getAppId(appName):
    logger("Looking for app...")
    reqURL=f"https://api.newrelic.com/v2/applications.json"
    try:
        response = requests.get(reqURL,
            params={'filter[name]': appName},
            headers={'Accept': 'application/json', 'X-Api-Key':os.environ.get('NEWRELIC_API_KEY')},
            timeout=5
        )
        json_response = response.json()
    except:
        #The request failed for some reason or other
        return False
    else:
        if("applications" in json_response):
            applications = json_response['applications']
            appID=0
            for app in applications:
                if(app['name'] == appName):
                    appID=app['id']
                    break
            return appID
        else:
            return 0



def createNodeApp(appName):
    logger("Sending traffic to node app")
    os.putenv("NEW_RELIC_LICENSE_KEY", APP_API_KEY)
    os.putenv("NEW_RELIC_APP_NAME", appName)
    os.system(f"cd {WORKING_DIRECTORY}/appstubs/node; node index.js")

def createJavaApp(appName):
    logger("Sending traffic to java app")
    os.putenv("NEW_RELIC_LICENSE_KEY", APP_API_KEY)
    os.putenv("NEW_RELIC_APP_NAME", appName)
    os.system(f"cd {WORKING_DIRECTORY}/appstubs/java; java -javaagent:{WORKING_DIRECTORY}/appstubs/java/newrelic/newrelic.jar StubApp > /dev/null")

def waitForApp(appName,attempts):
    if(attempts<=0):
        return 0

    if(APP_TYPE=="node"):    
        createNodeApp(appName)  # prod the app by sending it traffic
    if(APP_TYPE=="java"):
        createJavaApp(appName)
    time.sleep(WAIT_AFTER_CREATE)  

    foundApp=getAppId(appName)
    if(not(foundApp==0)):
        return foundApp
    else:
        logger("Waiting...")
        time.sleep(WAIT_BETWEEN_RETRIES)
        return waitForApp(appName,attempts-1)

def printApp(id):
    print(f"{{\"id\":\"{id}\"}}")
    exit(0)

# Look for app already existing
foundApp=getAppId(APP_NAME)
if(not(foundApp==0)):
    printApp(foundApp) 
else:
    foundApp=waitForApp(APP_NAME,RETRIES)
    if(not(foundApp==0)):
        printApp(foundApp)
    else:
        sys.stderr.write("App creation appears to have failed\n") 
        exit(1)
    


    
