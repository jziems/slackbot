import os
import json
import logging
from slack import RTMClient
from time import sleep
import asyncio

class ConfigurationError(Exception):
    def __init__(self, message):
        raise Exception(message)

class Slackbot(RTMClient):
    '''A simple Slack bot'''

    def __init__(self, configfile):
        try:
            if not os.path.isfile(configfile):
                raise ConfigurationError("Config file ({}) not found.".format(configfile))
            with open(configfile, 'r') as fin:
                self.cfg = json.load(fin)
            for k,v in self.cfg.items():
                setattr(self, k, v)
            sup = super()
            self.original_dispatch = sup._dispatch_event
            sup.__init__(token=self.token)
            sh = logging.FileHandler(filename=__package__ + '.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            sh.setFormatter(formatter)
            self._logger.addHandler(sh)
            self.on(event="message", callback=self.read)
        except:
            raise

    async def _dispatch_event(self, event, data=None):
        self._logger.debug("Event: '{}' Data: '{}'".format(event,data))
        await self.original_dispatch(event, data=data)

    def setloglevel(self, loglevel):
        self._logger.setLevel(loglevel)

    def read(self, **payload):
        data = payload['data']
        if 'user' in data.keys() and data['user'] != 'U29R3AQP6':
            self.post_message(channel='#bot_debug', text=data['text'])

    def post_message(self, channel=None, text=None, attachment=None, as_user=True):
        self._web_client.chat_postMessage(channel=channel, text=text, attachments=attachment, as_user=as_user)

    def list_channels(self):
        return self._web_client.channels_list()

    def list_users(self):
        return self._web_client.users_list()

    def channel_info(self, channel):
        return self._web_client.channels_info(channel=channel)

    def join_channel(self, channel):
        self._web_client.channels_join(channel=channel)

    def leave_channel(self, channel):
        self._web_client.channels_leave(channel=channel)

    def file_upload(self, file, channels, title=None):
        self._web_client.files_upload(channels=channels, file=file, title=title)

    def emojify(self, channel, emoji, timestamp):
        self._web_client.reactions_add(channel=channel, name=emoji, timestamp=timestamp)
