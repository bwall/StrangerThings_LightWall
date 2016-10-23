#!/usr/bin/env python2
import speech_recognition as sr
import time
from chatterbot import ChatBot
from string import ascii_lowercase

from Tkinter import *
from PIL import ImageTk, Image
import os
import traceback


class Viewer:
    def __init__(self, master):
        global APP_INSTANCE
        APP_INSTANCE = self
        self.top = master
        self.index = 0
        # display first image
        filename = "images/alphabet6.jpg"
        if not os.path.exists(filename):
            print "Unable to find %s" % filename
            self.top.quit()

        im = Image.open(filename)
        im = im.resize((self.top.winfo_screenwidth(), self.top.winfo_screenheight()))
        if im.format == "SPIDER":
            im = im.convert2byte()
        self.size = im.size
        self.tkimage = ImageTk.PhotoImage(im)

        self.lbl = Label(master, image=self.tkimage)
        self.lbl.pack(side="top")

        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source)

        self.stop_listening = r.listen_in_background(m, callback)

    # image doesn't appear unless put Image.open in separate function?
    # and need to use tkimage.paste, not ImageTk.PhotoImage
    def getImage(self, filename):
        im = Image.open(filename)
        im = im.resize((self.top.winfo_screenwidth(), self.top.winfo_screenheight()))
        if im.format == "SPIDER":
            im = im.convert2byte()
        return im

    def set_image_based_on_input(self, character):
        character = character.lower()
        if character not in ascii_lowercase:
            character = "6"

        im = self.getImage("images/alphabet{0}.jpg".format(character))
        self.tkimage.paste(im)

    def print_response(self, response):
        self.set_image_based_on_input("6")
        response = response.lower()
        for letter in list(response):
            self.set_image_based_on_input(letter)
            time.sleep(1.25)

            self.set_image_based_on_input("6")


APP_INSTANCE = None
r = None

MARKOV_BOT = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)
MARKOV_BOT.train("chatterbot.corpus.english")


def callback(recognizer, audio):
    message = None
    try:
        print "Attempting to resolve speech with Google Speech Recognition"
        message = recognizer.recognize_google(audio)
    except:
        print "Google Speech Recognition failed"
        try:
            print "Attempting to resolve speech with PocketSphinx (locally) (slow)"
            message = recognizer.recognize_sphinx(audio)
        except:
            traceback.print_exc()
            print "Sphinx failed, giving up"

    if message is None:
        print "Failed to hear text, QQ"
        return None
    else:
        print "You said: {0}".format(message)

    response = MARKOV_BOT.get_response(message)
    print "Bot response is: {0}".format(response)

    # pass to display
    APP_INSTANCE.print_response(str(response))


if __name__ == "__main__":
    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()
    root.bind("<Escape>", lambda e: e.widget.quit())
    app = Viewer(root)
    root.mainloop()
