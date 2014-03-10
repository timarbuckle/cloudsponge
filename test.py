#!/usr/bin/env python

import argparse
from ConfigParser import ConfigParser
import time
import sys

from cloudsponge import CloudSponge


def main(service):
    ## read config file for credentials
    cp = ConfigParser()
    cp.read('cloudsponge.conf')
    credentials = dict(cp.items('Credentials'))

    client = CloudSponge(credentials['domain_key'],
                         credentials['domain_password'])

    # initiate import, get redirect url
    resp = client.begin_import(service)
    import_id = resp['import_id']

    # wait for user to approve
    print 'import_id: {}'.format(import_id)
    print '      url: {}'.format(resp['url'])
    raw_input('Go to the url in your browser and grant permission. '
              'Press Enter when ready.')

    # poll until import success
    success = False
    loop = True
    while loop:
        resp = client.get_events(import_id)
        for event in resp['events']:
            print '{}: {}'.format(event['event_type'], event['status'])
            print '---'
            if event['status'] == 'ERROR':
                loop = False
                break
            if event['event_type'] == 'COMPLETE' and \
                    event['status'] == 'COMPLETED':
                success = True
                loop = False
                break
        time.sleep(1)

    # print results
    if success:
        resp = client.get_contacts(import_id)
        for contact in resp['contacts']:
            print '{} {}'.format(contact['first_name'],
                                 contact['last_name'])
            for email in contact['email']:
                print '    {}'.format(email['address'])
    else:
        print 'ERROR status detected'


if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = argparse.ArgumentParser(
        description='Test CloudSponge import client.')
    parser.add_argument('service', choices=['yahoo', 'gmail', 'windowslive'])
    args = parser.parse_args(sys.argv[1:])
    main(args.service.upper())
