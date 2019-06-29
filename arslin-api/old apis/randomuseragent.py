import random,requests, json

def LoadUserAgents():
    uafile='user_agents.txt'
    uas = []
    with open(uafile) as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1])
    random.shuffle(uas)
    return uas

def LoadProxies():
    proxyfile='proxies.txt'
    proxystring = []
    with open(proxyfile) as proxyf:
        for someprox in proxyf.readlines():
            if someprox:
                proxystring.append(someprox.strip()[1:-1])
    random.shuffle(proxystring)
    return proxystring


url = 'http://autos.vast.com/cars/api/'
uas = LoadUserAgents()
requestproxy = LoadProxies()
randomproxy = random.choice(requestproxy)
print(randomproxy)
proxy = {"http": "http://arslincars@gmail.com:vastmine@" + randomproxy}
ua = random.choice(uas)
headers = {
    "Connection" : "close",  # another way to cover tracks
    "User-Agent" : ua}
r = requests.get(url, proxies=proxy, headers=headers)
result = r.json()
print(result)