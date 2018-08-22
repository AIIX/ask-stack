import re
import sys
import json
import requests
import unidecode
from adapt.intent import IntentBuilder
from os.path import join, dirname
from string import Template
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import *
from mycroft.util import read_stripped_lines
from mycroft.util.log import getLogger
from mycroft.messagebus.message import Message

__author__ = 'aix'

LOGGER = getLogger(__name__)

class AskStackSkill(MycroftSkill):
    def __init__(self):
        super(AskStackSkill, self).__init__(name="AskStackSkill")
        self.client_secret = self.settings['client_secret']
        self.key = self.settings['key']

    @intent_handler(IntentBuilder("AskStackOverflow").require("AskStackOverflowKeyword").build())
    def handle_ask_stackoverflow_intent(self, message):
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(message.data.get('AskStackOverflowKeyword'), '')
        searchString = utterance.encode('utf-8')
        query = searchString.lstrip(' ')
        LOGGER.info(searchString)
        method = "GET"
        url = "https://api.stackexchange.com/2.2/search"
        data = "?order=desc&sort=activity&intitle={0}&site=stackoverflow&client_secret={1}&key={2}".format(query, self.client_secret, self.key)
        response = requests.request(method,url+data)
        global globalObject
        globalObject = response.json()
        resultCount = len(globalObject['items'])
        resultSpeak = "Displaying {0} Results".format(resultCount)
        self.speak(resultSpeak)
        self.enclosure.bus.emit(Message("stackresponseObject", {'desktop': {'data': response.text}}))
        
    def stop(self):
        pass
    
def create_skill():
    return AskStackSkill()
