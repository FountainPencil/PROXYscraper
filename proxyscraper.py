print("hello_world")
print("welcome to narnnia")
print("there is no place like home")
import urllib
import bs4 as bs
import pandas as pd
import json
import random
import os
import time
import sys

## json file check
def json_load():
    with open("proxydictlist.json") as f:
        print("json file exists")
        time.sleep(1)
        proxies_list = json.load(f)
        return proxies_list
def json_create():
    with open("proxydictlist.json", "w") as f:
        json.dump([], f)
        time.sleep(1)
        return

def json_config():
    with open('config.json', 'r') as f:
        doit = json.load(f)
        return doit

def json_makeconfig():
    for i in range(4):
        print("the following are case sensistive")
    config = {'URL': 'value0'}
    config = {'ProtocolColumnName': 'value1', 'IPAdressColumnName': 'value2', 'PortColumnName': 'value3'}
    config = {'key4': 'value4', 'key5': 'value5'}
    config = {'key6': 'value6', 'key7': 'value7'}
    config = {'key8': 'value8', 'key9': 'value9'}

    with open('config.json', 'w') as f:
        json.dump(config, f)
    config['URL'] = input("enterProxyurl:")
    config['ProtocolColumnName'] = input("EnterProtocolColumnName:")
    config['IPAdressColumnName'] = input("EnterIPAdressColumnName:")
    config['PortColumnName'] = input("EnterPortColumnName:")
    config['key4'] = input("enterProxyurl4:")
    config['key5'] = input("enterProxyurl5:")
    config['key6'] = input("enterProxyurl6:")
    config['key7'] = input("enterProxyurl7:")
    config['key8'] = input("enterProxyurl8:")
    config['key9'] = input("enterProxyurl9:")

    print("YOU MAY CHANGE THE CONFIG BY DELETING config.json")

    with open('config.json', 'w') as f:
        json.dump(config, f)
    print("YOU MAY CHANGE THE CONFIG BY DELETING config.json")
    return

if os.path.exists("proxydictlist.json"):
    proxies_list = json_load()
else:
    print("json file doesn't exist creating json file ...")
    json_create()
    proxies_list = json_load()

if os.path.exists("config.json"):
    print("config exists")
    doit = json_config()
else:
    print("NO CONFIG DATA")
    time.sleep(2)
    json_makeconfig()
    doit = json_config()
    for i in range(10):
        print("the following are case sensistive")


print(doit['ProtocolColumnName'])


print("*********************************************")
sys.exit("stopped code")

## getting the site
url = "https://free-proxy-list.net/" ## site containing the proxy.
print(f"attempting to connect to: {url}")
print(len(proxies_list))
if proxies_list: ## check if proxies_list is empty or not
    for i in range(0, len(proxies_list)):
        try:
            pick = random.choice(proxies_list)

            ## configuring urllib for use with proxies
            proxy_support = urllib.request.ProxyHandler(pick)
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)

            ## requests
            req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
            sauce = urllib.request.urlopen(req, timeout=5).read()
            soup = bs.BeautifulSoup(sauce, 'lxml')
            print(soup)
            break
        except:
            ## proxies that do not work are removed from the list
            print(f"{pick} did not work")
            proxies_list.remove(pick)
            print(f"{pick} removed")
            print(len(proxies_list))
            print(Exception)
else: ## if proxies_list is empty, we get our proxies without configuring urllib for using proxies
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    sauce = urllib.request.urlopen(req).read()
    soup=bs.BeautifulSoup(sauce, 'lxml')
    print(soup)

## use pandas to get tables and choose columns

df = pd.read_html(sauce) ## using pandas read_html method to parse through url
print(df, len(df))
df = df[0]  ## df is a list of tables. We want first table.

df.to_csv("proxiesraw.csv", index=True) ## saving df to csv

## print(df[0].columns) ## choosing dataframe with the index 0 and checking all the columns. You may need to check columns if name of column have weird spacing and etc.
## df = df[0] ## setting df as the df[0] the data frame with the ip, port, and etc.


df = pd.read_csv("proxiesraw.csv")
df = df[['IP Address', "Port", "Https"]]  ## making df only show the columns we want to see.
df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False) ## dropping all rows with missing values

def proxyINFO(df):
    proxyPort = df['Port'].tolist()        ## column "Port" to list
    proxyIP = df["IP Address"].tolist()    ## column "IP Address" to list
    HTTPS = df['Https'].tolist()           ## column "Https" to list
    HTTPS1 = []                            #3 empty list to make new list for "https" , "http"

    for item in HTTPS: ## convert HTTPS list with rows 'yes', 'no' to 'https', 'http' respectively and store them in HTTPS1 variable
        if item == "yes":
            print (item)
            HTTPS1.append("https")  ## i write it like this because I'm going to concat all three components later. Right now it should print "'https':https://"
        else:
            print(item)
            HTTPS1.append("http")
    print(proxyPort, proxyIP, HTTPS)
    return proxy_construct(proxyPort, proxyIP, HTTPS1)    ## this will start the next function and feed it the arguments proxyPort, ProxyIP, HTTPS1


def proxy_construct(proxyPort, proxyIP, HTTPS1):
    string = ":"
    proxyPort = [string + str(int(proxy)) for proxy in proxyPort] ## concat ":" at the start of each element in the list proxyPort
    ##print(HTTPS1)
    ##print(proxyPort)

    proxy_list = []
    for i in range(0, len(proxyPort)):      ## using for loop starting from 0 to size of proxyPort list. Doesn't matter which list you use. They should all be the same size
        PROXY = "http://" + proxyIP[i] + proxyPort[i]
        proxy_list.append(PROXY)
        print(PROXY)
    print(proxy_list)
    print(type(proxy_list))
    return proxy_dict(HTTPS1, proxy_list)

def proxy_dict(HTTPS1, proxy_list):
    proxies_dict_list = []
    for i in range(0, len(HTTPS1)):
        proxies_dict = {HTTPS1[i]: proxy_list[i]}
        proxies_dict_list.append(proxies_dict)
    return save_file(proxies_dict_list, HTTPS1, proxy_list)

def save_file(proxies_dict_list, HTTPS1, proxy_list):
    with open('proxydictlist.json', 'w') as f:
        json.dump(proxies_dict_list, f)
    proxy_list = pd.DataFrame(list(zip(HTTPS1,proxy_list)), columns=["https", "proxy"])
    proxy_list.to_csv("proxylist.csv", index=False)
    print("******************************************************")
    print(proxies_dict_list)
    print("******************************************************")
    print("scrape completed !")
proxyINFO(df)
