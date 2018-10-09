#!/usr/bin/env python3

import requests
import json
import sys
from collections import OrderedDict


def get_versions():
    url = 'https://api.github.com/repos/jenkinsci/swamp-plugin/releases'
    versions = set()
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()

        for rp in response:
            if 'tag_name' in rp.keys() and rp['tag_name'].startswith('swamp'):
                versions.add(rp['tag_name'].partition('swamp-')[-1])

    return versions


def get_stats():

    versions = get_versions()

    if isinstance(versions, str):
        versions = versions.split()

    stats = OrderedDict()

    for version in versions:
        data = {"type": "file",
                "repoKey": "releases",
                "path": "org/continuousassurance/swamp/jenkins/swamp/{version}/swamp-{version}.hpi".format(version=version)}

        response = requests.post('https://repo.jenkins-ci.org/ui/artifactgeneral', json=data)

        if response.status_code == 200:
            info = json.loads(response.text)
            stats['swamp-jenkins-plugin-{version}'.format(version=version)] = info['info']['downloaded']
        else:
            print(response, file=sys.stderr)

    return stats


if __name__ == '__main__':
    print(get_stats())
