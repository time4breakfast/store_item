#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import Storage as sto
import io

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


# noinspection PyPackageRequirements
class Storageassistant(object):
    """Class used to wrap action code with mqtt connection
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
            self.mystorage = sto.Storage()
        except :
            self.config = None

        # start listening to MQTT

        self.start_blocking()

    # --> Sub callback function, one per intent
    def additem_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        answer = self.mystorage.testing_dummy_function(intent_message) #addEntryToVorraete(intent_message.intent)

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, answer, "Storage_APP")

    def deleteitem_callback(self, hermes, intent_message):
        # terminate the session first if not continuechanged 'hello world' into 'guten tag'
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        answer = "Guten Tag"

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, answer, "Storage_APP")

    def checkamountofitem_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        # answer = self.mystorage.getAmountOf(intent_message)
        answer = self.mystorage.testing_dummy_function(intent_message)

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, answer, "Storage_APP")

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self, hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'time4breakfast:addItemToStorage':
            self.additem_callback(hermes, intent_message)
        elif coming_intent == '':
            self.deleteitem_callback(hermes, intent_message)
        elif coming_intent == 'time4breakfast:getAmountOfItem':
            self.checkamountofitem_callback(hermes, intent_message)

        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    Storageassistant()