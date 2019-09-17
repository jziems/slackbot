import json
import logging
from slack import WebClient,RTMClient

class ConfigurationError(Exception):
    def __init__(self, message):
        raise Exception(message)

class Slackbot:
    '''A simple Slack bot'''
    def __init__(self, configfile):
        try:
            self.logger = logging.getLogger(__name__)
            self.loglevel = logging.INFO
            sh = logging.FileHandler(filename=__name__ + '.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)
            with open(configfile, 'r') as fin:
                self.cfg = json.load(fin)
            for k,v in self.cfg.items():
                setattr(self, k, v)
            if not hasattr(self, 'SLACK_BOT_TOKEN') or not hasattr(self, 'BOT_ID'):
                raise ConfigurationError("Need SLACK_BOT_TOKEN and BOT_ID")
            if not hasattr(self, 'READ_WEBSOCKET_DELAY'):
                self.READ_WEBSOCKET_DELAY = 1
            self.web_client = WebClient(token=self.SLACK_BOT_TOKEN)
            self.rtm_client = RTMClient(token=self.SLACK_BOT_TOKEN)
            self.rtm_client.start()
        except Exception:
            raise

    def setloglevel(self, loglevel):
        self.logger.setLevel(loglevel)

    @RTMClient.run_on(event="message")
    def read(**payload):
        data = payload['data']
        web_client = payload['web_client']
        for k,v in data.items():
            print("{}: {}".format(k,v))

    def post_message(self, channel=None, text=None, attachment=None, as_user=True):
        self.web_client.chat_postMessage(channel=channel, text=text, attachments=attachment, as_user=as_user)

    def list_channels(self):
        return self.web_client.channels_list()

    def list_users(self):
        return self.web_client.users_list()

    def channel_info(self, channel):
        return self.web_client.channels_info(channel=channel)

    def join_channel(self, channel):
        self.web_client.channels_join(channel=channel)

    def leave_channel(self, channel):
        self.web_client.channels_leave(channel=channel)

    def file_upload(self, file, channels, title=None):
        self.web_client.files_upload(channels=channels, file=file, title=title)

    def emojify(self, channel, emoji, timestamp):
        self.web_client.reactions_add(channel=channel, name=emoji, timestamp=timestamp)