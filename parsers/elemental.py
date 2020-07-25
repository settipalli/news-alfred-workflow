# encoding: utf-8

import feedparser

from bs4 import BeautifulSoup


def get_data(*args):
    """
    Parse the One-Zero-Medium URL
    :return: {  title = news.text,
                subtitle= news.hyperlink,
                icon=ICON_WEB
             }
    """

    url = 'https://elemental.medium.com/feed/'

    feed = feedparser.parse(url)

    # # throw an error if request failed
    # # Workflow3 will catch this and show it to the user
    # r.raise_for_status()

    # extract news items
    result = []
    for news in feed.entries:
        result.append({
            'title': news.title.strip(),
            'subtitle': '{} - {}'.format(news['author'], news['published']),
            'link': news['link'],
        })

    return result


if __name__ == u'__main__':
    pass
