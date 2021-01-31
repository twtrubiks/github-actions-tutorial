import requests
import json
import os
from bs4 import BeautifulSoup
from linebot.models import TextSendMessage
from linebot import (
    LineBotApi, WebhookHandler
)

class SlackNotification:
    def __init__(self, context, slack_webhook):
        self.context = context
        self.slack_webhook = slack_webhook

    def push(self):
        slack_data = {
            "username": "NotificationBot",
            "icon_emoji": ":satellite:",
            "channel" : "#random",
            "attachments": [
                {
                    "color": "#a633ee",
                    "fields": [
                        {
                            "title": "New Incoming Message :zap:",
                            "value": self.context,
                            "short": "false",
                        }
                    ]
                }
            ]
        }
        headers = {'Content-Type': "application/json"}
        response = requests.post(self.slack_webhook, data=json.dumps(slack_data), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

class LineNotification:
    def __init__(self, Channel_Access_Token, context):
        self.line_bot_api = LineBotApi(Channel_Access_Token)
        self.context = context

    def push(self, target):
        self.line_bot_api.push_message(target, TextSendMessage(text=self.context))

class WebCrawler:
    def __init__(self):
        self.rs = requests.session()
        self.urls = [
            ('道瓊指數','https://invest.cnyes.com/index/GI/DJI'), # DJI
            ('S&P 500','https://invest.cnyes.com/index/GI/SPX'), # SPX
            ('美國那斯達克綜合指數','https://invest.cnyes.com/index/GI/IXIC'),# NASDAQ
            ('費城半導體','https://invest.cnyes.com/index/GI/SOX'),# 費城半導體
        ]
        self.result = []

    def fetch(self):
        for url in self.urls:
            res = self.rs.get(url[1], verify=False)
            soup = BeautifulSoup(res.text, 'html.parser')
            info_price = soup.select('.jsx-2941083017.info-price')[0].text
            info_change = soup.select('.jsx-2941083017.info-change')[0].text

            if '+' in info_change:
                info_change = info_change.split('+')
                info_change = '{}▲  {}▲'.format(info_change[1], info_change[2])
            else:
                info_change = info_change.split('-')
                info_change = '{}▼  {}▼'.format(info_change[1], info_change[2])

            self.result.append('{}\n{}\n{}'.format(url[0], info_price, info_change))

    def push(self, slack_webhook, line_token):
        result = '\n\n'.join(self.result)

        slack = SlackNotification(result, slack_webhook)
        slack.push()

        msg = LineNotification(line_token, result)
        # target = os.getenv('LINE_USER_ID')
        target = os.getenv('LINE_GROUP_ID')
        msg.push(target)

if __name__ == '__main__':
    crawler = WebCrawler()
    crawler.fetch()
    crawler.push(os.getenv('SLACK_WEBHOOK'), os.getenv('CHANNEL_ACCESS_TOKEN'))