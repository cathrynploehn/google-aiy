#!/usr/bin/env python3
# Cloudspeech Example Code by Cathryn Ploehn

import argparse
import locale
import logging
import schedule
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
    playMusic()

def ask_break():
    global musicPlaying
    
    logging.info("checking for break")

    if musicPlaying == False:
        aiy.voice.tts.say("don't forget to take a break.", "en-US", 50)
    else:
        logging.info("no break")

# play any wav file
def playSound(filename):
    # use FileZilla to load music
    #filename = "/home/pi/Music/neotibicen-pruinosus-loop.wav"
    aiy.voice.audio.play_wav(filename)

def stopMusic():
    global musicPlaying

    musicPlaying = False;
    leds.update(Leds.rgb_on((9, 99, 21)))
    logging.info("Music stopped")
    return schedule.CancelJob

# handles the listening and response
def playMusic():
    global client, leds, args, musicPlaying

    leds.pattern = Pattern.blink(500)
    leds.update(Leds.rgb_pattern((9, 99, 21)))

    if musicPlaying == False:
        logging.info("Playing music")
        playSound("/home/pi/Music/neotibicen-pruinosus-loop.wav")
        musicPlaying = True
        schedule.every(30).minutes.do(stopMusic)

# sets up the speech client
def main():
    global client, leds, args, musicPlaying

    board = Board()
    leds = Leds()
    musicPlaying = False;

    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    client = CloudSpeechClient('/home/pi/cloud_speech.json')

    board.button.when_pressed = _on_button_pressed
    leds.update(Leds.rgb_on((9, 99, 21)))

    schedule.every().hour.do(ask_break)

    logging.info('ready!!!!!!!!!')

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
