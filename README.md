# RoyalRoad_Downloader
Downloads a book on RoyalRoad and converts it to epub
By default the files will be created in D:/Books/RoyalRoad.

# How to use
python rr_downloader.py [OPTIONS] URL

  Parses the index at URL to fetch all the chapters of a book on RoyalRoad
  and store the content as epub.

Options:
  --out TEXT   Base output directory. A folder will be created for the book. Default: D:/Books/RoyalRoad
  --site TEXT  Base url of the website. Default: https://www.royalroad.com
  --help       Show this message and exit.
  
Example: python rr_downloader.py https://www.royalroad.com/fiction/21220/mother-of-learning