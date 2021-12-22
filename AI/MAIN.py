DATABASE = 'DATABASE.JSON'


import FRAMEWORK as _FRAMEWORK,Processor,COMMUNICATION,UpdateData
import json,os
import warnings

# Uncomment this bit out if you have the speech_recognition module installed,
# errors will occur if module not referenced as sr
import speech_recognition as sr

def startup():
    user_name = input(f'[Login]\nPlease enter your Username\n')
    with open(DATABASE,"r") as database:
        data = json.load(database)
        try:
            loops = 0
            found = data[user_name]
            while True:
                if loops > 0:
                    print('Incorrect Password! Please try again')
                pwd = input(f'Please enter your password\n')
                if pwd == data[user_name]["password"]:
                    return user_name
                loops += 1
        except:
            loops = 0
            _FRAMEWORK.DATA.create_directory(p=None,dir_name=user_name)
            print(f'Hello {user_name}!\n'
                  f'As a new user, I am required to have a password for your account.\n')
            while True:
                if loops > 0:
                    print('Your entries did not match! Please try again')
                entry = input(f'Please type a safe password to be linked with your account\n')
                s_entry = input(f'Please re-enter your password for confirmation\n')

                if entry == s_entry:
                    _FRAMEWORK.DATA.add_data(f'{user_name}', {"password": entry})
                    print('\nThank you! Your account is now setup and ready')
                    return user_name

                loops += 1

USER = startup()
UpdateData.USER = USER

__on__,input_type,botaudio = True,'typed',True

greet = COMMUNICATION.random_selection(COMMUNICATION.greeting_types, super=True)
COMMUNICATION.FORMAT.to_special(f'{greet} {USER}!', input_type=='audible')

def srcheck():
    try:
        import speech_recognition
        return True
    except:
        warnings.warn('Speech Recognition Module not enabled/installed')
        return False


while __on__:
    #For typing
    if input_type == 'typed':
        run = Processor.process(input(), USER,botaudio)
        if run == 'shutdown':
            break
        elif run == 'switch input':
            if srcheck():
                input_type = 'audible'
                COMMUNICATION.FORMAT.normal(f"Input switched to microphone")
        elif run == 'switch output':
            botaudio = not botaudio
            COMMUNICATION.FORMAT.normal(f'Bot audio switch to {botaudio}')

    #For microphone
    elif srcheck() and input_type == 'audible':
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=0.5)
            audio = r.listen(source)

        try:
            run = Processor.process(r.recognize_google(audio),USER, True)
            if run == 'shutdown':
                break
            elif run == 'switch input':
                input_type = 'typed'
                COMMUNICATION.FORMAT.normal(f"Input switched to typed", botaudio)
            elif run == 'switch output':
                botaudio = not botaudio
                COMMUNICATION.FORMAT.normal(f'Bot audio switch to {botaudio}')

        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            pass

COMMUNICATION.FORMAT.normal(f'Adios {USER}!',True)