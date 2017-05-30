"""
Main Web App for Alexa Skill
"""

import logging

# Local

# Third Party
import re

from flask import Flask
from flask_ask import Ask, statement

from dractor.dcim import Client

app = Flask(__name__)
ask = Ask(app, '/')

_CLIENT = None

@ask.intent('giggle')
def giggle():
    """
    Giggle Hertz
    :return:
    """

    speech_text = "Yes, I did say giggle hertz"

    return statement(speech_text).simple_card('Giggle', speech_text)

@ask.intent('getCPUModel')
def getCPUModel():
    """
    Return a card
    """

    cpu = _CLIENT.DCIM_CPUViewFactory.get('CPU.Socket.1')
    cpu_model = re.sub(r'v([0-9])', r'version \1', str(cpu.Model))
    cpu_model = re.sub(r'\(R\)', '', cpu_model)

    speech_text = "Your server contains an {}".format(cpu_model)

    return statement(speech_text).simple_card('CPU Model', speech_text)

@ask.intent('getSystemModel')
def getSystemModel():
    """
    Return the system
    :return:
    """

    my_system = _CLIENT.DCIM_SystemViewFactory.get('System.Embedded.1')

    speech_text = "Your server is made by {}.  It is a {}".format(my_system.Manufacturer,
                                                                my_system.Model)

    return statement(speech_text).simple_card('Server Model', speech_text)

@ask.intent('identify', mapping={'duration': 'duration'})
def identify(duration):
    """
    Turn on the chassis identify led
    """

    try:
        _CLIENT.DCIM_SystemManagementService.IdentifyChassis('Time Limited Enabled', DurationLimit=duration)
    except Exception:
        speech_text = "Hmm, I couldn't do that for some reason"
    else:
        speech_text = "I have turned on the blinky light for {} seconds".format(duration)

    return statement(speech_text).simple_card('Chassis Identify', speech_text)

@ask.intent('powerOn')
def power_on():

    try:
        _CLIENT.DCIM_CSPowerManagementService.RequestPowerStateChange(PowerState='2')
    except Exception:
        speech_text = "Hmm, maybe your server is already on?"
    else:
        speech_text = "I have turned on your server"

    return statement(speech_text).simple_card('Power On', speech_text)

@ask.intent('powerOff')
def power_off():

    try:
        _CLIENT.DCIM_CSPowerManagementService.RequestPowerStateChange(PowerState='8')
    except Exception:
        speech_text = "Hmm, maybe your server is already off?"
    else:
        speech_text = "I have turned off your server"

    return statement(speech_text).simple_card('Power Off', speech_text)


def main():
    """
    Console script entry point for debugging
    """

    global _CLIENT

    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.INFO)

    _CLIENT = Client('192.168.0.120', 443, 'root', 'calvin')
    _CLIENT.connect()


    app.run(debug=True)

if __name__ == '__main__':
    main()
