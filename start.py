import time
import argparse
import os
import requests
import base64
import hashlib
import sys
from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
import get_malicious
from abuseipdb import *
import apilityio
from threatminer import ThreatMiner

os.system('rm alert.txt')
a=open('output.txt','w')

otx = OTXv2("2e8bf67d611de674bd70308e0c48371a36b9ebf5847aa33f670efd0b2f2b9bf3")
ipdb = AbuseIPDB("c4530467d65eb608341f9054523ebdb6fe5000ed7fd8419512d6bf1b39f877fc08168f932fc524c0")
auth0ipdb = apilityio.Client(api_key='ec6bc49f-e8fc-43e1-aa79-435292f2d688')

def scan():
    ip=sys.argv[1]
    print("ALIENVAULT OTX STATS BEGIN")
    alienvault_alerts = get_malicious.ip(otx, ip)
    if len(alienvault_alerts) > 0:
        print("Alien valut detected this to be possibly malicious")
        #a.write(alienvault_alerts) #need to update writing modules
        print(alienvault_alerts)
    else:
        print("Safe to go from AlienVault")

    print("ABUSEIPDB STATS BEGIN")
    abuseibdb_alerts=ipdb.check(ip)
    score = abuseibdb_alerts.abuseConfidenceScore
    if score ==0:
        print("Safe according to AbuseIPDB")
    if score > 0 and score <=25:
        print("Seen few times, might want to have a look at it")
        print("Score is: "+str(score))
    if score > 25:
        #a.write("AbuseIPDB score: "+str(score)) need to update writing modules
        print("Abuse DB detected this to be possibly malicious")
        print("Abuse DB score: "+str(score))

    print("AUTH0 IP STATS BEGIN")
    auth0ipdb_alerts = auth0ipdb.CheckIP(ip)
    if auth0ipdb_alerts.status_code == 404:
        print("This IP has been cleared by AUTH0 Signal")
    if auth0ipdb_alerts.status_code == 200:
        print("Auth0 Signal has detected this to be possibly malicious")
        auth0_blacklists=auth0ipdb_alerts.blacklists
        print(auth0_blacklists)

    print("UNDER ATTACK STATS BEGIN")
    underattack_requests = requests.get('https://portal.underattack.today/api/lookup/ip/{0}'.format(ip),auth=requests.auth.HTTPBasicAuth('aashiq','Amma@2805'))
    #decide=input("Possible indicators found. Do you want to view and save them? [1 for yes, any thing else for no]")
    decide=1
    if decide == 1:
        underattack_alerts=underattack_requests.text
        print(underattack_alerts)

    print("THREAT MINER STATS BEGIN")
    threatminer_request=requests.get('https://api.threatminer.org/v2/host.php?q={0}&rt=4'.format(ip))
    #decide=input("Possible indicators found. Do you want to view and save them? [1 for yes, any thing else for no]")
    decide=1
    if decide==1:
        threatminer_alerts=threatminer_request.text
        print(threatminer_alerts)

    print("IBM X-FORCE EXCHANGE STATS BEGIN")
    XFE='python x_force.py -i '+str(ip)
    os.system(XFE)

#ip=input("Enter the ip to scan: ")
#ip=sys.argv[1]
#print("IP is successfully ingested. Starting now")
scan()
