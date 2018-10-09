import sys

import jenkins
import eclipse
import github
import sendmail
from collections import OrderedDict
import configparser


def get_stats(config):
    stats = OrderedDict()
    stats.update(jenkins.get_stats())
    stats.update(eclipse.get_stats('swamp-eclipse-plug'))
    stats.update(github.get_stats('swamp-scms-plugin', dict(config['GITHUB'])))
    stats.update(github.get_stats('java-cli', dict(config['GITHUB'])))
    return stats


def main(user_conf):

    config = configparser.ConfigParser()
    config.read(user_conf)

    stats = get_stats(config)

    sendmail.send(dict(config['MAIL-BOX']),
                  '\n'.join(['%s: %s' %
                             (key, stats[key]) for key in stats.keys()]))


if __name__ == '__main__':
    main(sys.argv[1])
