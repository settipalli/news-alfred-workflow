# encoding: utf-8

import importlib
import os
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

    if len(wf.args) == 0:
        # just list the news sources
        for source_name in news_sources.keys():
            wf.add_item(
                title=news_sources[source_name]['prefix'],
                subtitle=news_sources[source_name]['desc'],
                icon=os.path.join('icons', news_sources[source_name]['icon']),
                valid=False,
                autocomplete=news_sources[source_name]['uid'],
                uid=news_sources[source_name]['uid'],
            )

        # send results to Alfred as XML
        wf.send_feedback()
        return

    # get query from Alfred
    source_filter_query = None
    news_filter_query = None

    source_filter_query = wf.args[0]
    if len(wf.args) > 1:
        news_filter_query = u' '.join(wf.args[1:])

    filtered_source_names = news_sources.keys()

    if (source_filter_query):
        # fuzzy filter sources
        filtered_source_names = wf.filter(source_filter_query, news_sources.keys())

    for source_name in filtered_source_names:
        # retrieve posts from cache if available and no more than cacheForSecs old (usually, 1 minute)
        # if not, invoke the parser
        args = [news_sources[source_name]['parser']]
        news = wf.cached_data(source_name, get_news_from_parser, max_age=news_sources[source_name]['cacheforsecs'],
                              data_func_args=args)

        if (news_filter_query):
            news = wf.filter(news_filter_query, news, min_score=20, key=lambda news_item: u' '.join(news_item['title']))

        prefix = "[{0}] ".format(news_sources[source_name]['prefix'])
        for n in news:
            wf.add_item(
                title=n['title'],
                subtitle=u'{0} {1}'.format(prefix, n['subtitle']),
                icon=os.path.join('icons', news_sources[source_name]['icon']),
                arg=n['link'],  # tell alfred to pass the url to the next action in the workflow
                valid=True
            )

    # send results to Alfred as XML
    wf.send_feedback()


if __name__ == u'__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
