import requests
from bs4 import BeautifulSoup
import re

__all__ = ['Article', 'Content']

class Article():

    def __init__(self, url, title=None, img_url=None, preview_text=None, tag=None, label=None, class_name='article', id_name='main', video_page_url=None):

        self._url = url.replace('/gb/', '/b5/')
        self._title = title
        self._img_url = img_url
        self._preview_text = preview_text
        self._tag = tag
        self._label = label

        self._video_page_url = video_page_url.replace('/gb/', '/b5/') if video_page_url else video_page_url

        page = requests.get(self._url)
        self._soup = BeautifulSoup(page.text, 'html.parser')

        self._article = self._soup.find(class_=class_name)

        if not self._article:
            self._article = self._soup.find(id=id_name)

        if not self._article:
            self._article = self._soup.find('article')

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def title(self, class_name='title'):

        if not self._title:
            article_title = self._article.find(class_=class_name)
            self._title = article_title.text

        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def img_url(self, class_name='featured_image'):

        if not self._img_url:
            try:
                self._img_url = self._article.find(class_=class_name).find('a').get('href')
            except:
                try:
                    self._img_url = self._article.find(class_=class_name).find('figure').find('img').get('src')
                except:
                    try:
                        self._img_url = self._article.find(class_='wp-post-image').get('src')
                    except:
                        page = requests.get(self._video_page_url)
                        video_page_soup = BeautifulSoup(page.text, 'html.parser')
                        self._img_url = video_page_soup.select_one(f"a[href='{self._url}']").find('img').get('src')

        return self._img_url

    @img_url.setter
    def img_url(self, value):
        self._img_url = value

    @property
    def preview_text(self, id_name='artbody'):

        paragraph_index = 0

        while not self._preview_text:
            article_first_paragraph = self._article.find(id=id_name).find_all('p')[paragraph_index].text
            article_preview_text = re.sub(r'\【[^)]*\】', '', article_first_paragraph)
            article_preview_text = re.sub(r'\n', '', article_preview_text)
            article_preview_text = re.sub(r'\（英文大纪元[^)]*\编译）', '', article_preview_text)
            article_preview_text = re.sub(r'\（英文大紀元[^)]*\編譯）', '', article_preview_text)
            article_preview_text = re.sub(r'\（英國[^)]*\報導）', '', article_preview_text)
            article_preview_text = re.sub(r'\（大紀元[^)]*\報導）', '', article_preview_text)
            article_preview_text = re.sub(r'\(大紀元[^)]*\報導\)', '', article_preview_text)
            article_preview_text = re.sub(r'\（大纪元[^)]*\报导）', '', article_preview_text)
            article_preview_text = re.sub(r'\(大紀元[^)]*\報導）', '', article_preview_text)
            self._preview_text = article_preview_text.strip()
            paragraph_index += 1

        return self._preview_text

    @preview_text.setter
    def preview_text(self, value):
        self._preview_text = value

    @property
    def tag(self, id_name='breadcrumb'):

        if not self._tag:
            breadcrumb = self._soup.find(id=id_name)
            raw_tag = breadcrumb.findAll('a')[-1].text
            raw_tag = re.sub(r'\([^)]*\)', '', raw_tag)
            self._tag = re.sub(r'\（[^)]*\）', '', raw_tag)

        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value


class Content(Article):

    def __init__(self, article_url_list, video_url_list, video_page_url=None, advert=None):

        # parse data

        # article info
        self.article_list = [Article(article_url, video_page_url=video_page_url) for article_url in article_url_list]

        # video info
        self.video_list = [Article(video_url, video_page_url=video_page_url) for video_url in video_url_list]
        self.video_pair_list = [[value, self.video_list[counter+1]] for counter, value in enumerate(self.video_list) if counter%2 == 0]
        
        # advert info
        self.advert = advert


