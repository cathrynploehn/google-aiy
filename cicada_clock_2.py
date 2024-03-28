#!/usr/bin/env python3
# Cloudspeech Example Code by Cathryn Ploehn

import argparse
import locale
import logging
import time

import aiy.voice.tts
import aiy.voice.audio

from aiy.board import Board, Led
from aiy.leds import Leds, Color, Pattern
from aiy.cloudspeech import CloudSpeechClient

global client, leds, args

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

# trigger something when you press the button
def _on_button_pressed():
    leds.pattern = Pattern.blink(500)
    leds.update(Leds.rgb_pattern((9, 99, 21)))
    runConversation()

# play any wav file
def playSound():
    # use FileZilla to load music
    filename = "/home/pi/Music/neotibicen-pruinosus-loop-8.wav"
    aiy.voice.audio.play_wav(filename)

# handles the listening and response
def runConversation():
    global client, leds, args

    logging.info('Say something: play a sound, turn off the light, blink the light, turn on the light, say something')

    text = client.recognize(language_code=args.language, hint_phrases=None)

    if text is None:
        logging.info('You said nothing.')

    else:

        logging.info('You said: "%s"' % text)
        text = text.lower()

        # you can use any .wav file. Use Adobe Audition, etc. to convert files
        if 'what time is it' in text:
            playSound()
            leds.update(Leds.rgb_on((9, 99, 21)))

        # the robot can say anything in respose to any prompt. Build a conversation
        else:
            aiy.voice.tts.say("I don't know.", "en-US", 10)

        logging.info('Not listening')

# sets up the speech client
def main():
    global client, leds, args

    board = Board()
    leds = Leds()

    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    client = CloudSpeechClient('/home/pi/cloud_speech.json')

    board.button.when_pressed = _on_button_pressed
    leds.update(Leds.rgb_on((9, 99, 21)))

    logging.info('ready!!!!!!!!!')


if __name__ == '__main__':
    main()
