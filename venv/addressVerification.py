import requests
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree
import datetime
import time
import csv
import ConfigParser

print "'Tis but a scratch!' -  The Black Knight (Monty Python FC)"


# Default configuration of application, remains the same (more or less)
config = ConfigParser.ConfigParser()
config.read("/config.env")

USER = config.get('default', 'user') #['DEFAULT']['USER']
PWD = config['DEFAULT']['PWD']
CA_PATH = config['DEFAULT']['CA_PATH']
URL = config['DEFAULT']['URL']

# configuration for the document
PATH = config.get('DEFAULT', 'PATH')#config['DOCUMENT']['PATH']
SEARCH_LANG = config['DOCUMENT']['SEARCH_LANG']
MAX_ROWS = config['DOCUMENT']['MAX_ROWS']
SEARCH_TYPE = config['DOCUMENT']['SEARCH_TYPE']

addresses = []

def main():

    file_loader()

    row_Number = 0
    print addresses[0]

    for row_Number in addresses:
        # Variables for sending a request to the webservice
        name_request = str(row_Number[0])
        street_request = str(row_Number[1])
        houseNo_request = "481"
        postal_code_request = str(row_Number[3])
        town_request = str(row_Number[2])
        pbox_request = "0"
        pbox_nr_request = "0"

        # body of the actual XML request with the request variables filled in
        body = """<?xml version="1.0" encoding="UTF-8"?>
                 <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v4="http://post.ch/AdressCheckerExtern/V4-02-00">
                 <soapenv:Header/> <soapenv:Body>
                  <v4:AdressCheckerRequest>
                   <Params>
                     <MaxRows>""" + MAX_ROWS + """</MaxRows> 
                     <CallUser>""" + USER + """</CallUser>
                     <SearchLanguage>""" + search_lang + """</SearchLanguage>
                     <SearchType>""" + search_type + """</SearchType>
                   </Params>
                     <!--Optional:--><Names>""" + name_request + """</Names> 
                     <!--Optional:--> <Street>""" + street_request + """</Street> 
                     <!--Optional:--> <HouseNbr>""" + houseNo_request + """</HouseNbr> 
                     <!--Optional:--> <Onrp>0</Onrp> 
                     <!--Optional:--> <Zip>""" + postal_code_request + """</Zip> 
                     <!--Optional:--> <Town>""" + town_request + """</Town> <HouseKey>0</HouseKey> 
                     <!--Optional:--> <PboxAddress>""" + pbox_request + """</PboxAddress> 
                     <!--Optional:--> <PboxNbr>""" + pbox_nr_request + """</PboxNbr>
                  </v4:AdressCheckerRequest> </soapenv:Body>
                 </soapenv:Envelope>"""

        request_data(body)
        print body
        time.sleep(1)

def write_address_to_file(r):

    #writing full response to logfile for troubleshooting
    log_time = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    with open('/Users/blacksquirrelz/Documents/Python/validationAddress.txt', "a") as outfile:
        outfile.write(log_time + ': connection accepted, now verifying data! \n\n')
        outfile.write('Content: ' + r.content)
        outfile.write('\n\n**************************** End of request ********************************\n\n')

    root = ElementTree.fromstring(r.content)
    file_writer(root)

def write_error_to_logfile(message):
    # writing full responseto logfile for troubleshooting
    log_time = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    log_event = message

    with open('/Users/blacksquirrelz/Documents/Python/validationAddress.txt', "a") as outfile:
        outfile.write(log_time + ': Unexcpected exception \n\n')
        outfile.write(log_event)
        outfile.write('\n\n**************************** End of Exception ********************************\n\n')


def request_data(body):
    try:
        #Try to establish a connection with HTTPAuth.and check status code
        print 'Requesting data:\n'
        with requests.session() as s:
            s.post(URL, data=body, auth=HTTPBasicAuth(user, pwd))  # verify=CA_PATH,
        r = requests.post(URL, data=body, auth=HTTPBasicAuth(user, pwd))  # verify=CA_PATH

        if (r.status_code == 200):
            print "Connection accepted, data received:\n"
            write_address_to_file(r)
        else:
            #If the statuscode is not expected raise and log an exception into the logfile
            print "Connection denied, or unexpected HTML StatusCode, check next line for details:"
            print 'Status Code: ', r.status_code, '\nHeader: \n', r.headers, '\n\nContent: \n', r.content
            raise Exception
    except Exception:
        print Exception.message
        message = "Exception Message: " + str(Exception.message) + '\nStatus Code: ' + str(r.status_code) + '\nHeader: \n' + str(r.headers) + '\n\nContent: \n' + str(r.content)
        write_error_to_logfile(message)

def file_loader():

    #load the source file to the script
    file = open(PATH, 'r')
    reader = csv.reader(file, delimiter=',')
    next(reader)

    for row in reader:
        name = str(row[0])
        street = str(row[1])
        town = str(row[2])
        post_code = int(row[3])
        addresses.append([name, street, town, post_code])

    file.close()

def file_writer(result):
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
        verified_address = result

        writer.writerow([name, street, town, post_code, verified_address])

    return_file.close()

if __name__ == '__main__':
    main()