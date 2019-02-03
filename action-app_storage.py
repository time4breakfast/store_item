#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
# import io
from Storage import Storage

USERNAME_INTENTS = "time4breakfast"


def user_intent(intentname):
    return USERNAME_INTENTS + ":" + intentname

"""
def read_configuration_file(configuration_file):
    try:
        cp = ConfigParser.ConfigParser()
        with io.open(configuration_file, encoding="utf-8") as f:
            cp.readfp(f)
        return {section: {option_name: option.encode('utf8') for option_name, option in cp.items(section)}
                for section in cp.sections()}
    except (IOError, ConfigParser.Error):
        return dict()
"""

def subscribe_intent_callback(hermes, intent_message):
    # conf = read_configuration_file(CONFIG_INI)
    intentname = intent_message.intent.intent_name
    if intentname == user_intent("addItemToStorage"):
        result_sentence = mystorage.testing_dummy_function(intent_message)
        # item = [item.value for item in intent_message.slots.item.all()][0]
        # print(str(item))
        # result_sentence = item #'Hallo'
        hermes.publish_end_session(intent_message.session_id, result_sentence)


if __name__ == "__main__":
    mystorage = Storage()
    with Hermes("localhost:1883") as h:
        h.subscribe_intents(subscribe_intent_callback).start()
