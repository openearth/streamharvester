import requests
def search(service='ustream', keyword=None):
    if service == 'ustream':
        url  = 'http://api.ustream.tv/json/channel/live/search'
        if keyword:
            url += '/title:like:%s' % (keyword,)
        else:
            url += '/all'
    else:
        raise ValueError(service)
    return requests.get(url).json()
