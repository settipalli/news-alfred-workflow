# encoding: utf-8

import importlib
import sys

import yaml
from workflow import Workflow3

PARSERS_ROOT = 'parsers'

def get_news_from_parser(parser):
    parser = importlib.import_module('{0}.{1}'.format(PARSERS_ROOT, parser))
    news = parser.get_news()  # returns a list of dictionaries: [ { 'title': '', 'subtitle': '', 'icon': '' } ]
    return news

def main(wf):
    news_sources = yaml.safe_load(open("sources.yml"))

    for source_name in news_sources:
        # retrieve posts from cache if available and no more than cacheForSecs old (usually, 1 minute)
        # if not, invoke the parser
        args=[news_sources[source_name]['parser']]
        news = wf.cached_data(source_name, get_news_from_parser, max_age=news_sources[source_name]['cacheforsecs'], data_func_args=args)
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
