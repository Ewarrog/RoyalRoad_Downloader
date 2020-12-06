import settings
import click
import os
import requests
import re
from ebooklib import epub
from bs4 import BeautifulSoup
from tqdm import tqdm

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command()
@click.argument('url')
@click.option('--out', default=settings.DEFAULT_OUT_DIR, help='Base output directory.'
                                                              ' A folder will be created for the book')
@click.option('--site', default='https://www.royalroad.com', help='Base url of the website')
def download(**kwargs):
    """
    Parses the index at URL to fetch all the chapters of a book on RoyalRoad and store the content as epub.
    """
    
    output_dir = kwargs['out']
    os.makedirs(output_dir, exist_ok=True)

    html_text = requests.get(kwargs['url']).text
    soup = BeautifulSoup(html_text, 'html.parser')

    book_name = kwargs['url'].split('/')[-1]
    chapter_elements = soup.find_all('tr', attrs={'data-url': re.compile(r'/fiction/\d+/.+/chapter/\d+/.+')})
    epub_book = epub.EpubBook()
    epub_book.set_title(book_name)

    epub_chapters = []
    for chapter_id, chapter_elem in enumerate(tqdm(chapter_elements, desc='Processing chapters')):
        chapter_url = kwargs['site'] + chapter_elem.attrs['data-url']
        chapter_name = chapter_url.split('/')[-1]
        chapter_html = requests.get(chapter_url).text
        chapter_soup = BeautifulSoup(chapter_html, 'html.parser')
        chapter_content = chapter_soup.find(class_='chapter-inner chapter-content')

        new_soup = BeautifulSoup()
        html_tag = new_soup.new_tag('html')
        new_soup.append(html_tag)
        body_tag = new_soup.new_tag('body')
        body_tag['style'] = 'text-align: justify;margin:1em;'
        html_tag.append(body_tag)
        body_tag.append(chapter_content)

        epub_chapter = epub.EpubHtml(title=chapter_name, file_name=f'{chapter_id}_{chapter_name}.html')
        epub_chapter.set_content(new_soup.prettify())
        epub_chapters.append(epub_chapter)
        epub_book.add_item(epub_chapter)
    epub_book.toc = epub_chapters
    epub_book.spine = epub_chapters
    epub_book.add_item(epub.EpubNcx())
    epub_book.add_item(epub.EpubNav())
    epub.write_epub(os.path.join(output_dir, f'{book_name}.epub'), epub_book)


if __name__ == '__main__':
    download()
