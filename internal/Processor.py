#!/usr/bin/python3

if __name__ != '__main__':
    from internal import COMMUNICATION,UpdateData, DBManager, ARITHEMETIC
else:
    import COMMUNICATION,UpdateData, ARITHEMETIC, DBManager

import os,json
from random import randint,choice

DATABASE,AIAUDIOFILE = 'DATABASE.json','Sarah.mp3'

USER = None
botaudio, custom_library = False,False

extract = DBManager.extract

special_characters = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '-', '=', '[', ']', '{', '}', ';',
                      ':','|', ',', '<', '.', '>', '/', '?','_'
]

global math_keywords,convert_keywords,data_keywords
math_keywords,convert_keywords,data_keywords = {},{},{}
with open('internal/keywords.JSON','r') as f:
    KEYWORDS = json.load(f)
    math_keywords = KEYWORDS['math']
    convert_keywords = KEYWORDS['convert']
    data_keywords = KEYWORDS['data']
# Passive keywords is unsupported till future versions

custom_variables = {}


def group(collection):
    result = None
    for _ in [_ for i,_ in collection.items()]:
        if result:
            result = result + _
        else:
            result = _

    return result
_math_keywords,_data_keywords = group(math_keywords),group(data_keywords)#,group(convert_keywords)
                                       #^ _convert_keywords
                                       #v
KEYWORDS = _math_keywords+_data_keywords


def ContextV4(string):
    array = list(string)
    toReturn = []

    delim = 'OEBOFXO'
    delimat = []
    curIndex = 0
    ignore = set()

    userlib = DBManager.DATA.get(request=USER)
    global WORDS
    WORDS = KEYWORDS+list(userlib.keys())+list(custom_variables.keys())

    if custom_library:
        WORDS = list(set(WORDS)^set(_math_keywords))

    for keyword in WORDS:    # KEEP THIS ORDER (KEYWORDS,userlib.keys(),custom_variables.keys())
        foundAt = string.find(keyword,curIndex)

        while foundAt != -1 and foundAt not in ignore:
            # Duplicate case 1
            if foundAt+1 < len(string) and (keyword == '*' and string[foundAt+1] == '*'):
                break


            ignore.update(range(foundAt, foundAt+len(keyword)))
            delimat.append(foundAt)
            delimat.append(foundAt+len(keyword))
            curIndex = foundAt+1
            foundAt = string.find(keyword,curIndex)


        curIndex = 0

    # insert delims into array
    for i in reversed(sorted(delimat)):
        array.insert(i,delim)
        
    # join array and split by delims
    array = ''.join(array).split(delim)

    for i,text in enumerate(array):
        if not text:
            continue
        elif text not in KEYWORDS:
            toReturn += text.split()    #split normal words by white space
        else:
            text.lstrip(); text.rstrip() # removal left & right whitespace
            toReturn.append(text)

    # Get equations fix                                                                                # process is not custom
    toReturn = ARITHEMETIC.getEquations(toReturn, _math_keywords, custom_variables, _data_keywords) if not custom_library else toReturn
    return toReturn if toReturn != [] else None


def numify(num):
    num = custom_variables.get(num,num)
    try:
        return float(num)
    except:
        return num

def isNum(num):
    num = custom_variables.get(num,num)
    return isinstance(numify(num), (int,float))

def tryInt(num):
    num = custom_variables.get(num,num)
    if isNum(num) and int(num) == num:
        return int(num)
    else:
        return num
            
def custom_processing(context, deletion=False):
    global botaudio
        

    UpdateData.all(USER)

    '''Use of nicknames has been discontinued'''
    #global nickname
    #nickname = DBManager.DATA.get(f"{USER}.-custom-libray.nickname")

    articles = ['a','an','the']   # list of definte articles

    if context[0].lower() in data_keywords['dir_return']+data_keywords['pas_return']:
        context.pop(0)
        if not context: # context is empty
            return

    if context[0].lower() in articles:
        context.pop(0)
        if not context: 
            return

    text = ' '.join(context)
    lib = DBManager.DATA.get(request=f'{USER}.-custom-library')
    guess = False   # if request wasn't directly found

    
    if lib:
        find = lib.get(text)
        if find and deletion:
            find = text # set find to text for later confirmation

        elif not find:
            # Find first match
            for k,v in lib.items():
                find = k.find(text)
                if find != -1:
                    guess = True
                    if deletion:
                        find = k    # set find to key
                    else:
                        find = v    # set find to value
                    break
                else:
                    find = None

        if not lib or not find:
            COMMUNICATION.FORMAT.to_error(f"{text}, is not found in this library", out=botaudio)
            return

        
        if find:
            if deletion:
                # Should later support mic answers?
                answer = input(f'Delete {find}? [y/n]  -> ').lower()
                while answer not in ('y', 'yes', 'n', 'no'):
                    answer = input(f'Invalid answer\nDelete {find}? [y/n] -> ')

                if answer in ('y','yes'):
                    res = DBManager.DATA.remove_data(p=f'{USER}.-custom-library.{find}')
  
                                        # if res is None, succesful removal
                    COMMUNICATION.FORMAT.normal(res or f"{find}, has been removed from library",out=botaudio)

                else:   # must be n, or no
                    COMMUNICATION.FORMAT.normal(f"Removal cancelled",out=botaudio)
            else:
                find = find + ('?' if guess else '')
                COMMUNICATION.FORMAT.normal(f"{find}",out=botaudio)

def toBinaryOp(eq=[]):
    for i in range(len(eq)):
        _ = eq[i]
        if _ in math_keywords['dir_add']:
            eq[i] = '+'
        elif _ in math_keywords['dir_sub']:
            eq[i] = '-'
        elif _ in math_keywords['dir_mult']:
            eq[i] = '*'
        elif _ in math_keywords['dir_div']:
            eq[i] = '/'
        elif _ in math_keywords['dir_pow']:
            eq[i] = '^'
        elif _ in math_keywords['assignment']:
            eq[i] = '='

    return eq

def process(text,user, allowBotAudio=False,):
    global botaudio,custom_library, USER
    botaudio = allowBotAudio
    USER = user

    if text.lower() in ['shutdown','shut down']:
        return 'shutdown'
    elif text.lower() in ['switch output','switch bot audio']:
        return 'switch output'
    elif text.lower() in ['switch input']:
        return 'switch input'
    elif botaudio and text.lower() in ['repeat that','repeat','can you repeat that','could you repeat that','please repeat that']:
        os.system(AIAUDIOFILE)
        return
    elif text.lower() in ['sarah','sara']:
        a = ['Yes?','Uh huh?','Mm?','What?','Need something?','Hmm?',f'Yes {USER}?']
        COMMUNICATION.FORMAT.normal(choice(a),botaudio)
        return
    elif text.lower() in ['hey','hi','hello','howdy']:
        a = ['Hey','Hi','Hello','Howdy','Salutations']
        COMMUNICATION.FORMAT.normal(f'{choice(a)} {USER}!',botaudio)
        return

    context = ContextV4(text) # List of characters split and grouped into keywords, words or numbers

    #print(context) #FOR DEBUG

    if context is None:
        COMMUNICATION.FORMAT.to_error(f"Sorry, I don't understand", botaudio)
        return
    

    for index,_ in enumerate(context):
        lowered = _.lower() if type(_) is str else ''

        # Use Custom Library?
        if custom_library:
            if lowered in data_keywords['leave_CL']:
                custom_library = False
                COMMUNICATION.FORMAT.normal(f"Returning to default library", botaudio)
                return None #Finished
            elif lowered in data_keywords['add_to_CL']:
                # Label_Anser divide
                assign_syntax = -1
                j_context = ' '.join(context)
                try:
                    for case in ['is','equals','=','is equal to','is = to', 'is =']:
                        if j_context.find(case) != -1:
                            assign_syntax = case
                            break

                    assert assign_syntax != -1

                    as_i = context.index(assign_syntax)

                    Label = " ".join(context[index + 1:as_i])
                    Value = " ".join(context[as_i+1:])     # Possible out-of-range exepction

                    Value = custom_variables.get(Value,Value)   # Attempt to use Custom variable, else value

                    # remove odd punctuation
                    tostrip = ''.join(special_characters)
                    Label = Label.strip(tostrip)
                    Value = Value.strip(tostrip)

                    if Label and Value:

                        DBManager.DATA.add_data(f'{USER}.-custom-library', {Label: Value})
                        COMMUNICATION.FORMAT.normal(f"Given information has been learned", botaudio)
                except:
                    COMMUNICATION.FORMAT.to_error(f"Sorry, I don't understand", botaudio)


            elif lowered in data_keywords['del_from_CL']:
                try:
                    custom_processing(context[index+1:], deletion=True)
                except:
                    # (to delete) likely not specified
                    COMMUNICATION.FORMAT.to_error(f"Sorry, I don't understand", botaudio)
            else:
                custom_processing(context)

            return  # Quick fix to engage custom library only once       (Another Solution?)


        ##  IsMath?
        elif type(_) is list:
            _ = toBinaryOp(_)

            assign_to = _[0] if '=' in _ and _[0] else None

            # Check if assign_to is a number
            if isNum(assign_to) and not custom_variables.get(assign_to):
                COMMUNICATION.FORMAT.to_error(f'{assign_to} is a number and cannot be assigned',out=botaudio)
                continue

            # Check if assign_to is in user data
            if assign_to and DBManager.DATA.get(request=USER).get(assign_to):
                COMMUNICATION.FORMAT.to_error(f'{assign_to} is locked and cannot be assigned',out=botaudio)
                continue

            _ = _[2:] if assign_to is not None else _


            result = tryInt(ARITHEMETIC.solve(_))
            if assign_to:   # equation variable assignment
                result = result or _[-1]    # ... or simple 1:1 assignment
                custom_variables[assign_to] = result

                COMMUNICATION.FORMAT.normal(f'I have assigned {assign_to} to {result}', out=botaudio)
            
            elif result is not None: 
                COMMUNICATION.FORMAT.to_answer(result, botaudio)
            else:
                COMMUNICATION.FORMAT.to_error(f"Sorry, I don't understand", botaudio)

        elif lowered in data_keywords['dir_return']:    # Returning Data Queries
            UpdateData.all(USER)
            if not (index+1 < len(context)):
                return

            request = None
            if index+2 < len(context) and context[index+1] in ['the','my']:
                request = context[index+2]
            else:
                request = context[index+1]

            # base case
            if type(request) is not str:
                continue
            else:
                request = (request.lower()).strip(''.join(special_characters))


            if request in custom_variables:
                COMMUNICATION.FORMAT.normal(custom_variables.get(request),botaudio)
                continue

            # This is preferred to be checked after request in variables condition
            if isNum(request):
                COMMUNICATION.FORMAT.normal(request,botaudio)
                continue

            request = request.replace('_',' ')  # for linking multiple worded requests
            
            if request.lower() in ['name','username']:
                COMMUNICATION.FORMAT.normal(f'You are {USER}',botaudio)
                continue


            keys = DBManager.DATA.get(f'{USER}').keys()

            if request.lower() in keys:
                value = DBManager.DATA.get(f'{USER}.{request}')

                if request.lower() == 'password':
                    COMMUNICATION.FORMAT.to_special(f'That data is locked',botaudio)
                else:
                    result = DBManager.DATA.get(f'{USER}.{request}')
                    if result is not None:
                        c_request = request.split('_')
                        c_request = ' '.join(c_request)

                        if isinstance(result,(list,tuple,set)):
                            output = "{}".format(f'Your {c_request} are ' if context[index+1].lower() == 'my' else f'{c_request} are ')
                            COMMUNICATION.FORMAT.normal(
                                output + COMMUNICATION.FORMAT.to_group(result, rtn=True, alone=True),
                                botaudio)
                            pass
                        else:

                            output = "{}".format(f'Your {c_request} is ' if context[index+1].lower() == 'my' else f'{c_request} is ') + result
                            COMMUNICATION.FORMAT.normal(output,botaudio)
                    else:
                        COMMUNICATION.FORMAT.to_error(f"Seems I don't have that information. Sorry!",botaudio)

            elif index+2 < len(context) and context[index+1] == 'your': # TO BE IMPLEMENTED LATER
                COMMUNICATION.FORMAT.to_special('BOT DATABASE NOT YET IMPLEMENTED',botaudio)

        elif lowered == 'say':
            if index+1 < len(context):
                COMMUNICATION.FORMAT.normal(" ".join(context[index+1:]), botaudio)
                return  # only run once, maybe?
            else:
                COMMUNICATION.FORMAT.normal('What do you want me to say?', botaudio)

        elif lowered in data_keywords['enter_CL']:
            custom_library = True
            COMMUNICATION.FORMAT.normal("I am now linked to your custom library",botaudio)
            return