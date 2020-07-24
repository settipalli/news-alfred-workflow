# encoding: utf-8

from bs4 import BeautifulSoup
from workflow import web


def get_data(*args):
    """
    Parse The Hindu crunch URL
    :return: {  title = news.text,
                subtitle= news.hyperlink,
                icon=ICON_WEB
             }
    """

    url = 'https://www.thehindu.com/'

    r = web.get(url)

    # throw an error if request failed
    # Workflow3 will catch this and show it to the user
    r.raise_for_status()

    # extract news items
    soup = BeautifulSoup(r.text, 'html.parser')

    # with open('testdata-hacker-news.html') as f:
    #     soup = BeautifulSoup(f.read(), 'html.parser')

    result = []
    for news in soup.find_all('a', attrs={'data-vr-excerpttitle': True}):
        result.append({
            'title': news.text.strip(),
            'subtitle': news['href'],
            'link': news['href'],
        })

    return result


if __name__ == u'__main__':
    pass
