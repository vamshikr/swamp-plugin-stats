import sys
import os
import requests
from requests.auth import HTTPBasicAuth
from collections import OrderedDict


def get_release_stats(repository):
    stats = OrderedDict()

    url = 'https://api.github.com/repos/mirswamp/{repository}/releases'.format(repository=repository)

    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()

        for rp in response:
            if 'assets' in rp.keys() and len(rp['assets']) > 0:
                stats['{0}/{1}'.format(repository, rp['tag_name'])] = rp['assets'][0]['download_count']
    else:
        print(response)

    return stats


def get_clone_stats(repository, config):
    stats = OrderedDict()
    url = 'https://api.github.com/repos/mirswamp/{repository}/traffic/clones'.format(repository=repository)

    response = requests.get(url, auth=HTTPBasicAuth(config['username'], config['access_token']))

    if response.status_code == 200:
        rp = response.json()
        stats['{0}/{1}'.format(repository, 'clones')] = rp['count']
        return stats
    else:
        print(response)

    return OrderedDict()


def get_stats(repository, config):
    stats = OrderedDict()
    stats.update(get_release_stats(repository))
    stats.update(get_clone_stats(repository, config))
    return stats


if __name__ == '__main__':
    get_stat(sys.argv[1], sys.argv[2])
