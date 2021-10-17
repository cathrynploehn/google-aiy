#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Info about Neotibicen pruinosus (Say, 1925) from http://www.insectsingers.com/100th_meridian_cicadas/index.html
# more info: https://bugguide.net/node/view/6967
# more info: http://texasento.net/Cicada_TX.htm
# more songs here:  https://www.cicadamania.com/cicadas/cicada-songs-audio-sounds-noise/

import argparse
import locale
import logging
import time

import aiy.voice.tts
import aiy.voice.audio

from aiy.board import Board, Led
from aiy.leds import Leds, Color, Pattern
from aiy.cloudspeech import CloudSpeechClient

from threading import Timer,Thread,Event

global parser, args, hints, client, activeListening, board, leds, currTime, numRings
numRings = 18


def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('what time is it')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def _on_button_pressed():
    global activeListening, board, logging, leds

    if activeListening:
        activeListening = False
        logging.info('Not listening')
        # board.led.state = Led.ON
        leds.update(Leds.rgb_on((9, 99, 21)))
    else:
        activeListening = True
        # board.led.state = Led.BLINK;
        leds.pattern = Pattern.blink(500)
        leds.update(Leds.rgb_pattern((9, 99, 21)))
        runConversation()


class sunTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def checkTime():
    currTime = time.localtime()
    print(currTime)

    if currTime.tm_min == 59:
        ringCicada()

def ringCicada():
    sunrise = 7
    sunset = 20
    currTime = time.localtime()

    if currTime.tm_hour > sunrise and currTime.tm_hour < sunset:
        numRings = currTime.tm_hour - sunrise
        print(currTime.tm_hour)
        print(numRings)
        filename = "/home/pi/Music/neotibicen-pruinosus-loop-" + str(numRings) + ".wav"
        aiy.voice.audio.play_wav(filename)

def runConversation():
    global activeListening, board, args, hints, client, leds

    if hints:
        logging.info('Say something, e.g. %s.' % ', '.join(hints))
    else:
        logging.info('Say something.')


    text = client.recognize(language_code=args.language,
                            hint_phrases=hints)
    if text is None:
        logging.info('You said nothing.')
        # continue

    logging.info('You said: "%s"' % text)
    text = text.lower()
    # aiy.voice.tts.say(text)
    activeListening = False;

    if 'what time is it' in text:
        ringCicada()
        # aiy.voice.tts.say("It is time to call for a mate", "en-US", 10)
        # aiy.voice.audio.play_wav("/home/pi/neotibicen-pruinosus-wav.wav")

    #elif 'turn off the light' in text:
    #    board.led.state = Led.OFF
    #elif 'blink the light' in text:
    #    board.led.state = Led.BLINK
    # elif 'goodbye' in text:
    #     break

    # board.led.state = Led.ON
    leds.update(Leds.rgb_on((9, 99, 21)))
    logging.info('Not listening')

def main():
    global args, hints, client, parser, board, activeListening, leds

    activeListening = False
    board = Board()
    leds = Leds()
    #leds.update(Leds.rgb_on((9, 99, 21)))

    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient('/home/pi/cloud_speech.json')

    board.button.when_pressed = _on_button_pressed
    leds.update(Leds.rgb_on((9, 99, 21)))
    # board.led.state = Led.ON;
    # aiy.voice.tts.say("I am the cicada.", "en-US", 10)

    logging.info('ready!!!!!!!!!')

    t = sunTimer(60,checkTime)
    t.start()
    ringCicada()


if __name__ == '__main__':
    main()
