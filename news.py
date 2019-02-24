# encoding: utf-8

import importlib
import sys

import yaml
from workflow import Workflow3

PARSERS_ROOT = 'parsers'


def main(wf):
    news_sources = yaml.safe_load(open("sources.yml"))

    for source_name in news_sources:
        # invoke the parser
        parser = importlib.import_module('{0}.{1}'.format(PARSERS_ROOT, news_sources[source_name]['parser']))
        news = parser.get_news()  # returns a list of dictionaries: [ { 'title': '', 'subtitle': '', 'icon': '' } ]

        for n in news:
            wf.add_item(
                title=n['title'],
                subtitle='[{0}] {1}'.format(source_name, n['subtitle']),
                icon=n['icon'],
                arg=n['subtitle'], # tell alfred to pass the url to the next action in the workflow
                valid=True
            )

    # send results to Alfred as XML
    wf.send_feedback()


if __name__ == u'__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
