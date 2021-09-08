# -*- coding: utf-8 -*-
# @Time  : 2021/3/16 14:06
# @Author : lovemefan
# @File : thaudiotruyen.py
import requests

from utils.MediaDownloader import MediaDownloader
from bs4 import BeautifulSoup

class ThMediaTruyen(MediaDownloader):
    """website : https://thaudiotruyen.com/
    downloader the audios
    """
    def __init__(self):
        self.web_url = 'https://thaudiotruyen.com/'
        self.book_categories = {'truyen-hot': 'https://thaudiotruyen.com/truyen-hot/trang-1',
                                'kiem-hiep': 'https://thaudiotruyen.com/the-loai/kiem-hiep/trang-1',
                                'tien-hiep': 'https://thaudiotruyen.com/the-loai/tien-hiep/trang-1',
                                'huyen-huyen': 'https://thaudiotruyen.com/the-loai/huyen-huyen/trang-1',
                                'do-thi': 'https://thaudiotruyen.com/the-loai/do-thi/trang-1',
                                'xuyen-khong': 'https://thaudiotruyen.com/the-loai/xuyen-khong/trang-1'
                               }

    def download(self):

        for category, url in self.book_categories.items():
            next_page = url
            while True:
                html = requests.get(next_page).text
                bs = BeautifulSoup(html, "html.parser")
                books = bs.select('.thumb_img')
                next_page = bs.select('a[rel="next"]')
                for book in books:
                    book_name = book.contents[1]['href'][1:]
                    book_url = self.web_url + '/' + book_name
                    book_html = html = requests.get(book_url).text

                if len(next_page) != 0:
                    break



if __name__ == '__main__':
    downloader = ThMediaTruyen()
    downloader.download()