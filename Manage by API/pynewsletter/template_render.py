# for rendering html template with Jinja
from jinja2 import Environment, FileSystemLoader
import os
from .content_script import Content

# for viewing the email draft in webpage
import webbrowser
from datetime import date


__all__ = ['Jinja_Template']

class Jinja_Template(Content):

    def __init__(self,
                 template_folder_name = 'Jinja Templates',
                 template_file_name = 'newsletter_as_jinja_template_base.html'):

        file_loader = FileSystemLoader('../'+template_folder_name+'/')
        self.env = Environment(loader=file_loader, extensions=['jinja2.ext.do'])

        # render the base template
        self.template = self.env.get_template(template_file_name)

    def render(self, source_contect,
               folder_name='Exported HTML',
               rendered_newsletter_filename = 'rendered_newsletter.html'):

        # description: subject_line and preview_text
        self.subject_line = source_contect.article_list[0].title
        article_title_list = [article.title for article in source_contect.article_list]
        self.preview_text = ' · '.join(article_title_list[1:])

        self.rendered_content = self.template.render(env=self.env,
                                                   header=source_contect.article_list[0],
                                                   article_list=source_contect.article_list,
                                                   video_pair_list=source_contect.video_pair_list,
                                                   advert=source_contect.advert)

        self.folder_path = '../' + folder_name + '/'

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        self.newsletter_path = self.folder_path + rendered_newsletter_filename

        with open(self.newsletter_path, "w") as fh:
            fh.write(self.rendered_content)

        print('newsletter rendered at: '+ self.newsletter_path)

    def preview(self):

        webbrowser.open('file://' + os.path.realpath(self.newsletter_path))
