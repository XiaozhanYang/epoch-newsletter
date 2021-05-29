# for building and sending emails with MailChimp
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json

__all__ = [MailChimp_Campaign]

class MailChimp_Campaign(Jinja_Template):

    def __init__(self, newsletter, mailchimp_config,
                 # sender information
                 from_name='Anonymous Sender',
                 reply_to='no_reply@email.com'):

        self.subject_line = newsletter.subject_line
        self.preview_text = newsletter.preview_text
        self.rendered_content = newsletter.rendered_content
        self.mailchimp_config = mailchimp_config

        # sender information
        self.from_name = from_name
        self.reply_to = reply_to

        # campaign name
        today = date.today().strftime("%d %B %Y")
        self.campaign_title = 'Campaign_Created_through_API' + today

    def connect_to_MailChimp(self):

        self.client = MailchimpMarketing.Client()
        self.client.set_config({
            "api_key": self.mailchimp_config["API_KEY"],
            "server": self.mailchimp_config["API_KEY"].split('-')[-1]
        })

        response_ping = self.client.ping.get()

        if response_ping['health_status'] == "Everything's Chimpy!":
            print("MailChimp account connected!")

    def update_MailChimp_template(self):

        response = self.client.templates.update_template(
            self.mailchimp_config['template_id'], {"name": "Template_Created_through_API", "html": self.rendered_content})
        print("Template updated at:", response['date_edited'])

    def specify_recipients(self):

        if self.mailchimp_config['segment_id']:
            self.recipients = {'segment_opts':
                               {'saved_segment_id':
                                   self.mailchimp_config['segment_id']},
                               'list_id': self.mailchimp_config['list_id']}
        else:
            self.recipients = {'list_id': self.mailchimp_config['list_id']}

        print('recipients specified.')

    def create(self):

        self.connect_to_MailChimp()
        self.update_MailChimp_template()
        self.specify_recipients()

        self.created_campaign = self.client.campaigns.create({"type": "regular",
                                                              'recipients': self.recipients,
                                                              "settings":
                                                              {"title": self.campaign_title,
                                                               "subject_line": self.subject_line,
                                                               "preview_text": self.preview_text,
                                                               "from_name": self.from_name,
                                                               "reply_to": self.reply_to,
                                                               "template_id": self.mailchimp_config['template_id'],
                                                               "auto_footer": False}})
        print('Campaign created successfully!')

    def send(self):

        campaign_id = self.created_campaign['id']
        response_of_campaigns_send = self.client.campaigns.send(campaign_id)

        return response_of_campaigns_send


