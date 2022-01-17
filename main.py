#!/usr/bin/python3
DATABASE = 'DATABASE.JSON'
try:
    open(DATABASE).close()
except:
    with open(DATABASE,'w') as db:  # To initialize a database if none exists
        db.write('{}')

from internal import DBManager as DBManager,Processor,COMMUNICATION,UpdateData
import warnings


__on__,input_type,botaudio = True,'typed',False

def startup():
    COMMUNICATION.FORMAT.normal('Login. Please enter your Username', out=botaudio)
    user_name = input(f'[Login]\nPlease enter your Username -> ')
    user = DBManager.DATA.get(user_name)
    if user: # TYPE: DICT
        COMMUNICATION.FORMAT.normal('Please enter your password', out=botaudio)
        pwd = input(f'Please enter your password -> ')

        while pwd != user['password']:
            COMMUNICATION.FORMAT.to_error('Error, Incorrect Password! Please try again', out=botaudio)
            print('\nError, Incorrect Password! Please try again')

            COMMUNICATION.FORMAT.normal('Please enter your password', out=botaudio)
            pwd = input(f'Please enter your password -> ')
        return user_name


    COMMUNICATION.FORMAT.normal(f'Hi {user_name}, it is nice to meet you! As a new user, I am required to have a password for your account.', out=botaudio)
    print(f'Hello {user_name}!\nAs a new user, I am required to have a password for your account.\n')
    
    # NO PASSWORD CHECKER (lazy)
    COMMUNICATION.FORMAT.normal('Please type a safe password to be linked with your account', out=botaudio)
    new_pwd = input(f'Please type a safe password to be linked with your account -> ')

    COMMUNICATION.FORMAT.normal('Please re-enter your password for confirmation', out=botaudio)
    confirm_pwd = input(f'Please re-enter your password for confirmation -> ')


    while new_pwd != confirm_pwd:
        COMMUNICATION.FORMAT.to_error('ERROR. Your entries did not match! Please try again', out=botaudio)
        print('\nERROR! Your entries did not match! Please try again')

        COMMUNICATION.FORMAT.normal('Please type a safe password to be linked with your account', out=botaudio)
        new_pwd = input(f'Please type a safe password to be linked with your account -> ')

        COMMUNICATION.FORMAT.normal('Please re-enter your password for confirmation', out=botaudio)
        confirm_pwd = input(f'Please re-enter your password for confirmation -> ')

    DBManager.DATA.create_directory(p=None,dir_name=user_name)
    DBManager.DATA.add_data(p=f'{user_name}', new_data={"password": new_pwd})
    DBManager.DATA.create_directory(p=f'{user_name}',dir_name='-custom-library')  # create custom library directory

    for preset_data in 'morning,afternoon,night,evening,meridiem,time,date,today,day,month,year,thread,process,system flags'.split(','):
        DBManager.DATA.add_data(p=f'{user_name}', new_data={preset_data:''})

    COMMUNICATION.FORMAT.normal('Thank you! Your account is now setup and ready', out=botaudio)
    print('\nThank you! Your account is now setup and ready\n')
    return user_name


USER = startup()  # USER is just user's user_name
UpdateData.USER = USER
print()
greet = COMMUNICATION.random_selection(COMMUNICATION.greeting_types, super=True)
COMMUNICATION.FORMAT.to_special(f'{greet}, {USER}!', botaudio)

def srcheck():
    try:
        import speech_recognition as sr
        return sr
    except:
        warnings.warn('Speech Recognition Module not enabled/installed')
        return False

value_error = False

sr = srcheck()
r = sr.Recognizer() if sr else None
Microphone = sr.Microphone() if sr else None
check = r and Microphone

while __on__:
    print()   # So each run output is seperated
    #For typing
    if input_type == 'typed':
        run = Processor.process(input('-> '), USER, botaudio)
        if run == 'shutdown':
            break
        elif run == 'switch input':
            if check:
                input_type = 'audible'
                COMMUNICATION.FORMAT.normal(f"Input switched to microphone", out=botaudio)
        elif run == 'switch output':
            botaudio = not botaudio
            COMMUNICATION.FORMAT.normal(f'Bot audio switch to {botaudio}', out=False)

    #For microphone
    elif input_type == 'audible':
        try:
            with Microphone as source:
                r.adjust_for_ambient_noise(source,duration=0.5)
                audio = r.listen(source)

                text = r.recognize_google(audio)
                COMMUNICATION.FORMAT.normal(f'{text}?', out=botaudio)
                run = Processor.process(text,USER, botaudio)
                if run == 'shutdown':
                    break
                elif run == 'switch input':
                    input_type = 'typed'
                    COMMUNICATION.FORMAT.normal(f"Input switched to typed", out=botaudio)
                elif run == 'switch output':
                    botaudio = not botaudio
                    COMMUNICATION.FORMAT.normal(f'Bot audio switch to {botaudio}', out=False)

                value_error = False
        except sr.UnknownValueError as e:
            if not value_error:
                COMMUNICATION.FORMAT.normal(f'Sorry, I don\'t understand', out=botaudio)
                value_error = True
        except sr.RequestError as e:
            pass


goodbye = COMMUNICATION.random_selection(COMMUNICATION.goodbye_types, super=True)
COMMUNICATION.FORMAT.to_special(f'{goodbye}, {USER}!', out=botaudio)