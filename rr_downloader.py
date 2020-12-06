import subprocess

import click
import os
import requests
import re
from bs4 import BeautifulSoup

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command()
@click.argument('url')
@click.option('--out', default='D:/Books/RoyalRoad/', help='Base output directory.'
                                                           ' A folder will be created for the book')
@click.option('--site', default='https://www.royalroad.com', help='Base url of the website')
def download(**kwargs):
    """
    Parses the index at URL to fetch all the chapters of a book on RoyalRoad and store the content as html.
    The html file is then converted to epub format using Calibre's "ebook-convert" command.
    (Calibre must have been previously installed https://calibre-ebook.com/fr/download)
    """
    try:
        subprocess.run(['ebook-convert', '-h'])
    except FileNotFoundError:
        print('Calibre must be intalled to use ebook-convert to convert html files to epub. You can get it at '
              'https://calibre-ebook.com/fr/download')
        input("Press Enter to continue...")
        return 1

    html_text = requests.get(kwargs['url']).text
    soup = BeautifulSoup(html_text, 'html.parser')

    book_name = kwargs['url'].split('/')[-1]
    chapter_elements = soup.find_all('tr', attrs={'data-url': re.compile(r'/fiction/\d+/.+/chapter/\d+/.+')})

    idx = 1

    for chapter_elem in chapter_elements:
        chapter_url = kwargs['site'] + chapter_elem.attrs['data-url']
        chapter_name = chapter_url.split('/')[-1]
        chapter_html = requests.get(chapter_url).text
        chapter_soup = BeautifulSoup(chapter_html, 'html.parser')
        chapter_content = chapter_soup.find(class_='chapter-inner chapter-content')
        html_path = os.path.join(kwargs['out'], book_name, 'raw_html', f'{idx}_{chapter_name}.html')
        epub_path = os.path.join(kwargs['out'], book_name, 'epub', f'{idx}_{chapter_name}.epub')

        new_soup = BeautifulSoup()
        html_tag = new_soup.new_tag('html')
        new_soup.append(html_tag)
        body_tag = new_soup.new_tag('body')
        body_tag['style'] = 'text-align: justify;'
        html_tag.append(body_tag)
        body_tag.append(chapter_content)

        os.makedirs(os.path.dirname(html_path), exist_ok=True)

        with open(html_path, 'w') as f:
            f.write(new_soup.prettify())

        os.makedirs(os.path.dirname(epub_path), exist_ok=True)

        print(f'Running ebook-convert {html_path} {epub_path}')
        subprocess.run(['ebook-convert', html_path, epub_path])

        idx += 1


if __name__ == '__main__':
    download()
