import sys
import csv
import re
from telnetlib import NOP
import requests
from requests.auth import HTTPProxyAuth
import socket
from progress.bar import Bar
from time import sleep
import os
import urllib3
urllib3.disable_warnings()

os.system('') #  #enable VT100 Escape Sequence for WINDOWS 10

# load the domains.csv file into a list

domain_list = []
filename = 'domains.csv'

# load the csv into a list of dictionaries
def load_csv(filename):
    with open(filename, 'r',  encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain_list.append(row)

    return domain_list


ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_RESET = "\033[0m"
ANSI_WHITE = "\033[37m"

FAKE_USERAGENT = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



session = requests.Session()
# session.proxies = {'http': 'http://147.135.1.151:3129', 
#                     'https': 'http://147.135.1.151:3129'}
# session.auth = HTTPProxyAuth("hideipvpn@wlmedia.com", "securepass")
# # session.trust_env=False

def color_print(text, color, newline = True):
    if newline:
        print('\n')
    print(color + text + ANSI_RESET, end ="")
    if newline:
        print('\n')


domain_list = load_csv(filename)    


# print(domain_list)

# define a check_domain function that takes a dictionary of domain and keyword as argument
# return false for errors
def check_domain(domain):
    domain_name = domain['Domain']
    keyword = domain['keyword']
    host = domain['host']

    # check if the domain is up

    try:
    
        ip = socket.gethostbyname(domain_name)
        # print('[+] ' + domain_name + ' is up!')
                
    except Exception as e:
        color_print ('[-] ' + domain_name + '('+host+')' +' not resolved with exception '+ str(e), ANSI_RED)
        return False

    # use requests to load the home page of the domain
    # try and catch to handle errors
    try:

        # do a reqeusts get via a proxy
        # proxy = {'http': 'http://

        r = session.get('https://www.' + domain_name, headers = FAKE_USERAGENT, timeout=(10, 30), verify=False) # 10 second connect timeout, 30 second read timeout
        # print(r.status_code)
        if r.status_code == 200:

            # check if the keyword is in the home page
            if keyword in r.text:
                # print('[+] ' + domain_name + ' has the keyword ' + keyword)
                return True
            else:
                color_print('[-] ' + domain_name + '('+host+')' +' does not have the keyword ' + keyword, ANSI_RED)
                return False
        else:                
            color_print('[-] ' + domain_name + '('+host+')' +' status code is ' +r.status_code, ANSI_RED)
            return False




    except Exception as e:
        color_print(f'[-] {domain_name}({host}) is down with exception {str(e)}', ANSI_RED)
        return False


# escape fo rmodule if main
if __name__ == '__main__':
    
    # if arg contains --verbose then set verbose flag
    verbose = False
    if len(sys.argv) > 1 and sys.argv[1] == '--verbose':
        verbose = True

    if verbose:
        print('Verbose mode is on')


    color_print ('[+] Starting check of {} domains...'.format(len(domain_list)), ANSI_WHITE)
    error_count = 0
    with Bar('Checking', fill='>', max = len(domain_list), suffix='%(percent).1f%% - ETA %(eta)ds') as bar:
        # iterate through domain_list and check domain for each one
        for domain in domain_list:
            # color_print('.', ANSI_GREEN, False)
            if verbose:
                print('Checking ' + domain['Domain'])
            if not check_domain(domain):
                error_count += 1
            bar.next()
        bar.finish()
    
    # print done in green

    if error_count == 0:
        color_print ('[+] All domains are up and running!', ANSI_GREEN)
    else:
        color_print ('[-] There were {} domains that were down'.format(error_count), ANSI_RED)
    

