import csv
import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint

from xml.etree import ElementTree

addresses = []
rowNumber = 0

path = "/Users/blacksquirrelz/Documents/Python/Addresses.csv"
file = open(path, 'r')
reader = csv.reader(file, delimiter=',')
header = next(reader)

for row in reader:
    name = str(row[0])
    street = str(row[1])
    town = str(row[2])
    post_code = int(row[3])
    addresses.append([name, street, town, post_code])

#print len(addresses)
#print addresses[0]

user = "TU_61428_0001"
pwd = "B92vH3v6"
certificate = '/Users/blacksquirrelz/Documents/Python/_Server_Gold_G2_.ca'

#Check the address with the webservice
url="http://webservices.post.ch"

headers = {'content-type': 'application/soap+xml'}
#headers = {'content-type': 'text/xml'}
body = """<?xml version="1.0" encoding="UTF-8"?>
         <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v4="http://post.ch/AdressCheckerExtern/V4-02-00">
         <soapenv:Header/> <soapenv:Body>
          <v4:AdressCheckerRequest>
           <Params>
             <MaxRows>100</MaxRows> 
             <CallUser>TU_61428_0001</CallUser>
             <SearchLanguage>1</SearchLanguage>
             <SearchType>1</SearchType>
           </Params>
             <!--Optional:--><Names>Felix Muster</Names> 
             <!--Optional:--> <Street>Viktoriastrasse.</Street> 
             <!--Optional:--> <HouseNbr>21</HouseNbr> 
             <!--Optional:--> <Onrp>0</Onrp> 
             <!--Optional:--> <Zip>3013</Zip> 
             <!--Optional:--> <Town>Bern</Town> <HouseKey>0</HouseKey> 
             <!--Optional:--> <PboxAddress>0</PboxAddress> 
             <!--Optional:--> <PboxNbr></PboxNbr>
          </v4:AdressCheckerRequest> </soapenv:Body>
         </soapenv:Envelope>"""
try:
    authentication_response = requests.get('https://webservices.post.ch', verify=certificate, auth=HTTPBasicAuth(user, pwd))
    authRespRoot = ElementTree.fromstring(authentication_response.content)
    print authRespRoot

    #print authentication_response.text
    if("env:Client" in authentication_response.text):
        raise Exception
    else:
        validationFunction()
except Exception:
    print "Raised exception"
finally:
    #for testing purposes, take out once completed
    response = requests.post(url, data=body, headers=headers)
    root = ElementTree.fromstring(response.content)
    #print response.content
    print "Root Element:  ", root.tag
    print "Faultcode:  ", root[0][0][1].tag, root[0][0][1].text
    print "Content: ", response.content
    #until here is testing

#parse response
def validationFunction():
    response = requests.post(url, data=body, headers=headers)
    root = ElementTree.fromstring(response.content)
    print "Root Element:  ", root



#store to file

return_file = "/Users/blacksquirrelz/Documents/Python/VerifiedAddresses.csv"
file = open(return_file, 'w')
writer = csv.writer(file)
writer.writerow(["Name", "Street", "Town", "PLZ", "Verified Address"])

for i in range(len(addresses)):
    current_row = addresses[i]
    name = current_row[0]
    street = current_row[1]
    town = current_row[2]
    post_code = current_row[3]
    verified_address = "Test"

    writer.writerow([name, street, town, post_code, verified_address])
