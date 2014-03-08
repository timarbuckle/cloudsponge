#!/usr/bin/env python


import requests


class CloudSponge:
    """
    Python Client for the CloudSponge Contact Importer API
    """

    class Services(object):
        yahoo = 'YAHOO'
        gmail = 'GMAIL'
        windowslive = 'WINDOWSLIVE'

    def __init__(self, domain_key, domain_password, api_format='.json'):
        self.credentials = {
            'domain_key': domain_key,
            'domain_password': domain_password
        }
        self.api_format = api_format

    def get_url(self, urlname, import_id=None):
        base_url = 'https://api.cloudsponge.com'
        urls = {
            "begin_import": "{}/begin_import/user_consent{}",
            "get_events": "{}/events{}",
            "get_contacts": "{}/contacts{}"
        }

        if urlname in urls:
            url = urls[urlname].format(base_url, self.api_format)
            if import_id:
                url = '{}/{}'.format(url, import_id)
        else:
            url = None
        return url

    def begin_import(self, service, opt_include=None,
                     opt_user_id=None, opt_echo=None):

        payload = self.credentials
        payload['service'] = service

        url = self.get_url('begin_import')
        r = requests.get(url, params=payload)
        return r.json()

    def get_events(self, import_id):
        url = self.get_url('get_events', import_id)
        r = requests.get(url, params=self.credentials)
        return r.json()

    def get_contacts(self, import_id):
        url = self.get_url('get_contacts', import_id)
        r = requests.get(url, params=self.credentials)
        return r.json()


def main():
    from ConfigParser import ConfigParser
    cp = ConfigParser()
    cp.read('cloudsponge.conf')
    credentials = dict(cp.items('Credentials'))
    client = CloudSponge(credentials['domain_key'],
                         credentials['domain_password'])
    #resp = client.begin_import(client.Services.yahoo)
    #import_id = resp['import_id']
    #print 'import_id: {}'.format(import_id)
    #print 'url: {}'.format(resp['url'])
    #print 'Go to the url in your browser and grant permission. '
    #      'Press Enter when ready.'

    import_id = '31133771'
    resp = client.get_events(import_id)
    print resp
    #client.begin_import(client.Services.gmail, opt_format='.xml')
    #client.begin_import(client.Services.windowslive)

if __name__ == '__main__':
    main()
