#!/usr/bin/python3
DATABASE = 'DATABASE.json'
AIAUDIO = 'Sarah.mp3'

import os,time,sys,warnings


answer_types = {
'intro': [
    'That would be ', "I believe that's ", "Pretty sure it's ", "I'm certain that it's ",
    'It has got to be ', "Surely it's "
],
'outro': [
    ' I believe.', ' if I remember correctly.', ' surely ', ''
]
}

greeting_types=['Hello','How may I be of service','Hi']
goodbye_types=['See you later', 'Bye now', 'Adios', 'Farewell']


from MODULES.gtts import gTTS
from MODULES.mutagen.mp3 import MP3

def thenaudio(t):
    # Defaulted to english Version 1.0.0
    try:
        tts = gTTS(text=t, lang='en')
        tts.save(AIAUDIO)
        time.sleep(0.2) # fixes stutter?
        os.system(AIAUDIO)
        audio = MP3(AIAUDIO)
        time.sleep(audio.info.length)
    except:
        warnings.warn('GTTS or mutagen modules not enabled/installed')
        print('\nSpeech: ',t)


from random import randint
def random_selection(collection,super=False):
    if isinstance(collection, list):
        # IDEK it just does super? random selection and doesnt bug so all is well
        return random_selection(collection[randint(0,len(collection)-1)],True) if super else collection[randint(0,len(collection)-1)]
    elif isinstance(collection,dict):
        # same here
        if super:
            c = [v for i, v in collection.items()]
            return random_selection(c[randint(0,len(c)-1)],True)
        else:
            c = [[i, v] for i, v in collection.items()]
            return c[randint(0,len(c)-1)]
    else:
        return collection


def greet(name, out=False, rtn=False):
    name = str(name)
    b, e = '~| ', ' |~'
    b, e = '', ''
    output = random_selection(greeting_types)
    if out:
        thenaudio("".join([b, output, name, e]))
    else:
        if rtn:
            return "".join([b, output, name, e])
        else:
            print("".join([b, output, name, e]))



def goodbye(name, out=False, rtn=False):
    text = str(name)
    b, e = '~| ', ' |~'
    b, e = '', ''
    output = random_selection(goodbye_types)
    if out:
        thenaudio("".join([b, output, name, e]))
    else:
        if rtn:
            return "".join([b, output, name, e])
        else:
            print("".join([b, output, name, e]))


class FORMAT:
    @staticmethod
    def to_special(text, out=False, rtn=False):
        text = str(text)
        b,e = '~| ',' |~'
        b, e = '', ''
        if out:
            thenaudio("".join([b,text,e]))
        else:
            if rtn:
                return "".join([b,text,e])
            else:
                print("".join([b, text, e]))

    @staticmethod
    def to_error(text,out=False, rtn=False):
        text = str(text)
        b, e = '!| Error ', " |!"
        b, e = '', ''
        if out:
            thenaudio("".join([b,text,e]))
        else:
            if rtn:
                return "".join([b,text,e])
            else:
                print("".join([b,text,e]))

    @staticmethod
    def to_answer(text,out=False, rtn=False):
        text = str(text)
        b, e = '~| ',' |~'
        b, e = '', ''
        a_t = random_selection(answer_types)
        if a_t[0] == 'intro':
            output = random_selection(answer_types['intro'])
            text_char = list(text)
            text_char[0] = text_char[0].lower()
            text = ''.join(text_char)
            if out:
                thenaudio("".join([b, output, text, e]))
            else:
                if rtn:
                    return "".join([b, output, text, e])
                else:
                    print("".join([b, output, text, e]))
        else:
            if a_t[0] == 'outro':
                output = random_selection(answer_types['outro'])
                if out:
                    thenaudio("".join([b, text, output, e]))
                else:
                    if rtn:
                        return "".join([b, text, output, e])
                    else:
                        print("".join([b, text, output, e]))

    @staticmethod
    def normal(text,out=False, rtn=False):
        text = str(text)
        b,e = '| ',' |'
        b, e = '', ''
        if out:
            thenaudio("".join([b,text,e]))
        else:
            if rtn:
                return "".join([b,text,e])
            else:
                print("".join([b,text,e]))

    @staticmethod
    def to_group(collection,out=False, rtn=False,alone=False):

        collection = [str(el) for el in collection]

        b, e = '| ', ' |'
        b, e = '', ''
        limit = 10

        text = ', '.join(collection[:limit if limit < len(collection) else None])

        if len(collection) > limit:
            text += f' and {len(collection) - limit} more items'

        if out and not alone:
            thenaudio("".join([b,text,e]))
        elif not alone:
            if rtn:
                return "".join([b,text,e])
            else:
                print("".join([b,text,e]))
        elif out and alone:
            thenaudio(text)
        elif alone:
            if rtn:
                return text
            else:
                print(text)
