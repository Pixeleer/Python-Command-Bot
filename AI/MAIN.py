DATABASE = 'DATABASE.JSON'
from AI import FRAMEWORK as _FRAMEWORK,Processor,COMMUNICATION,UpdateData
import json,os,speech_recognition as sr
r = sr.Recognizer()

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
greet = COMMUNICATION.random_selection(COMMUNICATION.greeting_types,True)
COMMUNICATION.FORMAT.to_special(f'{greet} {USER}!',True)


__on__,input_type = True,'type'
while __on__:
    #For typing
    if input_type == 'type':
        run = Processor.process(input(), USER)
        if run == 'shutdown':
            break
        elif run == 'switch input':
            input_type = 'mic'
            COMMUNICATION.FORMAT.normal(f"Input switched to microphone",True)

    #For microphone
    if input_type == 'mic':
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=0.5)
            audio = r.listen(source)

        try:
            run = Processor.process(r.recognize_google(audio),USER)
            if run == 'shutdown':
                break
            elif run == 'switch input':
                input_type = 'type'
                COMMUNICATION.FORMAT.normal(f"Input switched to typed", True)
        except sr.UnknownValueError:
            __excuse__ = None
        except sr.RequestError as e:
            __excuse__ = None

COMMUNICATION.FORMAT.normal(f'Adios {USER}!',True)