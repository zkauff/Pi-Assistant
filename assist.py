
import time
import sys
import threading
import speech_recognition as sr
from rivescript import RiveScript

import os 
commands = ["takeoff", "land", "up", "down", "left", "turn", "touchdown", "exit", "flip", "barrel roll", "record",
            "exit", "emergency", "end recording", "playback"]

GOOGLE_CLOUD_SPEECH_CREDENTIALS = os.system['GOOGLE_CREDENTIALS']
if not GOOGLE_CLOUD_SPEECH_CREDENTIALS:
    print("Please set environment variable for cloud credentials.")
    exit(1)

def main():
    command = ""
    playback_mode = 0
    record_mode = 0
    finished_playback = 0
    file_name = "record-log.txt"
    recognizer = sr.Recognizer()
    sr.pause_threshold = 0.5

    riveBot = RiveScript()
    riveBot.load_directory("./commands")
    riveBot.sort_replies()

    while True:
        use_command = 1
        if playback_mode == 0:
            commands = voice_command(recognizer).split("and")
        else:
            f = open(file_name, "r")
            commands = f.readlines()
        for command in commands:
            simplified_command = riveBot.reply("localUser", command)
            command = simplified_command.rstrip()
            if "exit" in simplified_command:
                break

def voice_command(r):
    while True:
        # loop back to continue to listen for commands if unrecognizable speech is received
        with sr.Microphone() as source:
            print("Waiting for command...")
            r.pause_threshold = 0.5
            if voice_command.adjust_ambient_noise_flag is True:
                r.adjust_for_ambient_noise(source, duration=1)
                voice_command.adjust_ambient_noise_flag = False
            audio = r.listen(source)
        try:
            print("Command received. Processing...")
            command = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS,
                                               preferred_phrases=commands).lower()
            print('You said: ' + command + '\n')
            return command
        except sr.UnknownValueError:
            print('Didn\'t understand that, try again...')


voice_command.adjust_ambient_noise_flag = True

main()
