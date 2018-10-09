import sys
import re

import bs4
import requests
from collections import namedtuple
from collections import OrderedDict
import pdb


def get_stats(plugin):

    page = requests.get('https://marketplace.eclipse.org/content/' + plugin)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table')

    EclipseStats = namedtuple('EclipseStats', ['date', 'ranking', 'installs', 'clickthroughs'])

    header = [c.getText() for c in table.find('thead').find('tr').children if isinstance(c, bs4.element.Tag)]

    eclipse_stats = OrderedDict()

    for row in table.find('tbody').find_all('tr'):
        children = list(row.children)
        stat = EclipseStats(children[0].getText(),
                            children[1].getText(),
                            children[2].getText(),
                            children[3].getText())

        #[c.getText() for c in table.find('tbody').find('tr').children if isinstance(c, bs4.element.Tag)]

        match = re.match(r'(?P<num>\d+)\s*.*', stat.installs)
        if match:
            eclipse_stats['swamp-eclipse-plugin/{date}'.format(date=stat.date)] = match.groupdict()['num']

    return OrderedDict({k:eclipse_stats[k] for k in list(eclipse_stats.keys())[:3]})


if __name__ == '__main__':
    print(get_stats(sys.argv[1]))
