# RoyalRoad_Downloader
Downloads a book on RoyalRoad as html and then converts it to epub (needs Calibre)
By default the files will be created in D:/Books/RoyalRoad.
A folder will be created for the book and the html files will be in a "raw_html" folder and the epub files will be in an "epub" folder.

# How to use
python rr_downloader.py [OPTIONS] URL

  Parses the index at URL to fetch all the chapters of a book on RoyalRoad
  and store the content as html. The html file is then converted to epub
  format using Calibre's "ebook-convert" command. (Calibre must have been
  previously installed https://calibre-ebook.com/fr/download)

Options:
  --out TEXT   Base output directory. A folder will be created for the book. Default: D:/Books/RoyalRoad
  --site TEXT  Base url of the website. Default: https://www.royalroad.com
  --help       Show this message and exit.
  
Example: python rr_downloader.py https://www.royalroad.com/fiction/21220/mother-of-learning