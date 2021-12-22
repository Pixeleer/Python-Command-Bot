DATABASE,AIAUDIO = 'DATABASE.json','Sarah.mp3'

import COMMUNICATION,FRAMEWORK as _FRAMEWORK,UpdateData
import json,os,math as _math,time
from random import randint,choice

audible = False

allowed_context = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y',
                   'z','_',"'",'"'
]
special_characters = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '-', '=', '[', ']', '{', '}', ';',
                      ':','|', ',', '<', '.', '>', '/', '?'
]
math_keywords = {
    'dir_add': ['plus','+','combined with','joined with'],
    'pas_add': ['add','combine','join', 'sum of'],
    'dir_sub' : ['minus','-','taken from'],
    'pas_sub': ['subtract','take','negate'],
    'dir_mult': ['times', '*'],
    'pas_mult': ['product of', 'multiple of'],
    'dir_div': ['divided by', '/', 'over'],
    'pas_div': ['quotient of'],
    'dir_pow': ['^', '**','to the power of','to the'],
}

convert_keywords = {'dir_pow_flex': ['squared','tripled','quadrupled','turkied']}
data_keywords = {
    'dir_return': ['get',"what's",'what is','who is','what are','what does'],
    'pas_return': ['can i have','can you tell me'],
    'enter_PS': ['personal setting', 'personal settings','enter personal setting', 'open personal setting', 'enter personal', 'open personal'],
    'leave_setting': ['exit','leave setting','exit setting'],
    'add_INFO': ['learn','acknowledge']
}
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
    toReturn = list()

    delim = 'OEBOFXO'
    delimat = list()
    curIndex = 0
    ignore = list()

    for keyword in KEYWORDS:
        foundAt = string.find(keyword,curIndex)
        while foundAt != -1 and foundAt not in ignore:
            # Duplicate case 1
            if keyword == '*' and string[foundAt+1] == '*':
                break
            ignore += range(foundAt, len(keyword))
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
        if text == '':
            # array.remove(text) no need
            continue
        elif text not in KEYWORDS:
            toReturn += text.split()
        else:
            toReturn.append(text) 

    return toReturn


def numify(num):
    num = custom_variables.get(num,num)
    try:
        try:
            return int(num)
        except:
            return float(num)
    except:
        return num

def isNum(num):
    num = custom_variables.get(num,num)
    try:
        try:
            if int(num):
                return True
        except:
            if float(num):
                return True
    except:
        return False 

def round(num):
    num = custom_variables.get(num) or num
    if isNum(num) and int(num) == num:
        return int(num)
    else:
        return num


'''def conversion(INFO,WON):
    # Unpack conversion info
    a,conv = INFO

    if conv in convert_keywords['dir_pow_flex']:
        a = WON or custom_variables.get(a,a)

        try:
            a = numify(a)
            if conv == 'squared':
                return round(a**2)
            elif conv == 'tripled':
                return round(a**3)
            elif conv == 'quadrupled':
                return round(a**4)
            elif conv == 'turkied':
                return round(a**5)
        except:
            COMMUNICATION.FORMAT.to_error(f'Could not bring {a} to power',audible)'''

def math(e,WON):
    # Unpack mathematical info
    a,op,div,b = None,None,None,None
    if len(e) == 3:     # Direct equation
        a,op,b = e
    elif len(e) == 4:   # Passive equation
        op,a,div,b = e

    if op in math_keywords['dir_add']:
        # Set a to WON|look for custom_variable a|use a, Look for custom_variable b|use b
        a,b = WON or custom_variables.get(a,a), custom_variables.get(b,b)

        try:
            return round(numify(a)+numify(b))
        except:
            try:
                return a+b
            except:
                COMMUNICATION.FORMAT.to_error(f'Unable to add {a} and {b}',audible)
    elif op in math_keywords['pas_add']:
        a,b = WON or custom_variables.get(a,a), custom_variables.get(b,b)
        try:
            return round(numify(a)+numify(b))
        except:
            try:
                return a+b
            except:
                COMMUNICATION.FORMAT.to_error(f'Unable to add {a} and {b}', True)

    elif op in math_keywords['dir_sub']:
        a,b = WON or custom_variables.get(a,a), custom_variables.get(b,b)
        try:
            a,b = numify(a), numify(b)
            if div == 'taken from':
                return round(b-a)
            else:
                return round(a-b)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to subtract {a} and {b}', audible)
    elif op in math_keywords['pas_sub']:
        a,b = WON or custom_variables.get(a,a), custom_variables.get(b,b)

        try:
            a,b = numify(a),numify(b)
            if div == 'from':
                return round(b-a)
            else:
                return round(a-b)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to subtract {a} and {b}',audible)
    
    elif op in math_keywords['dir_mult']:
        a,b = WON or custom_variables.get(a,a), custom_variables.get(b,b)
        custom_variables.get(b)

        try:
            a,b = numify(a), numify(b)
            return round(a*b)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to multiply {a} and {b}', audible)
    elif op in math_keywords['pas_mult']:
        a,b = WON or custom_variables.get(a,a), custom_variables.get(b,b)

        try:
            a,b = numify(a), numify(b)
            return round(a*b)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to multiply {a} and {b}', audible)

    elif op in math_keywords['dir_div']:
        a,b = WON or custom_variables.get(a,a), custom_variables.get(b,b)

        try:
            return round(numify(a)/numify(b))
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to divide {a} and {b}', audible)
    elif op in math_keywords['pas_div']:
        a,b = WON or custom_variables.get(a,a), custom_variables.get(b,b)

        try:
            return round(numify(a)/numify(b))
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to divide {a} and {b}', audible)

    elif op in math_keywords['dir_pow']:
        a,b = WON or custom_variables.get(a,a), custom_variables.get(b,b)

        try:
            return round(numify(a)**numify(b))
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to bring {a} to the power of {b}', audible)

def learner_processing(text,user):
    UpdateData.all()
    global nickname
    nickname = _FRAMEWORK.DATA.get(f"{user}.personal.nickname")
    text = text.lower()
    with open(DATABASE,'r') as r_database:
        data = json.load(r_database)
        for Label,Value in data[user]['personal'].items():
            try:
                result = text.find(Label)
                if result != -1:
                    def extract(collection, isdict=False):
                        a = list()
                        if isdict:
                            for key, _ in collection.items():
                                if isinstance(_, (int, str)):
                                    a.append(_)
                                elif isinstance(_, (list, tuple, set, dict)):
                                    a = a + extract(_, isinstance(_, dict))
                        else:
                            for _ in collection:
                                if isinstance(_, (int, str)):
                                    a.append(_)
                                if isinstance(_, (list, tuple, set, dict)):
                                    a = a + extract(_, isinstance(_, dict))
                        return a

                    if isinstance(Value, dict):
                        x = extract(Value, isinstance(Value, dict))
                        COMMUNICATION.FORMAT.to_group(f"{x} {nickname}",out=True)
                    elif isinstance(Value,list):
                        x = COMMUNICATION.FORMAT.to_group(Value, rtn=True,alone=True)
                        COMMUNICATION.FORMAT.normal(f"{x} {nickname}",audible)
                    else:
                        COMMUNICATION.FORMAT.normal(f"{Value} {nickname}",audible)
                    return None
            except:
                __excuse__ = None
        COMMUNICATION.FORMAT.normal(f"I don't know {text}", audible)


personal,adding = False,False
def process(text,user, isAudible=False):
    audible = isAudible # global varaiable 
    if text.lower() in ['shutdown','shut down']:
        return 'shutdown'
    elif text.lower() in ['switch input']:
        return 'switch input'
    elif text.lower() in ['repeat that','repeat','can you repeat that','could you repeat that','please repeat that']:
        os.system(AIAUDIO)
        return
    elif text.lower() in ['sarah','sara']:
        a = ['Yes?','Uh huh?','Mm?','What?','Need something?','Hmm?',f'Yes {user}?']
        COMMUNICATION.FORMAT.normal(choice(a),audible)
        return
    elif text.lower() in ['hey','hi','hello','howdy']:
        a = ['Hey!','Hi!','Hello!','Howdy!','Salutations!',f'Hi {user}!']
        COMMUNICATION.FORMAT.normal(choice(a),audible)
        return
    global personal,adding


    context = ContextV4(text) # List of characters split and grouped into keywords, words or numbers
    print(context)
    if context is None:
        COMMUNICATION.FORMAT.to_error(f"There was an error comprehending some of your words I'm afraid", audible)
        return
    
    
    if personal:
        for index,_ in enumerate(context):
            if _.lower() in data_keywords['leave_setting']:
                personal = False
                COMMUNICATION.FORMAT.normal(f"Ok, I'm no longer learning", audible)
                return None #Finished
            elif _.lower() in data_keywords['enter_PS']:
                adding = True
                if _.lower() == 'done':
                    adding = False
                    break
                i = index
                while i < len(context):
                    if context[i] not in ['is', 'equals']:
                        i += 1
                    else:
                        break

                Label = " ".join(context[index + 1:i])
                i += 1
                Value = ""
                while i < len(context):
                    Value += f'{context[i]} '
                    i += 1
                if Label and Value != "":
                    _FRAMEWORK.DATA.add_data(f'{user}.personal', {Label: Value})
                    COMMUNICATION.FORMAT.normal(f"Information learned", audible)
        if not adding:
            learner_processing(text,user)
        adding = False
        return None  # Finished

    # won abbreviates 'Working On Number'
    WON = None
    #WOKW = None
    for index,_ in enumerate(context):


        lowered = _.lower() #Implement this new change#

        ##  IsMath?
        if lowered in _math_keywords:
            
            if index+1 < len(context):  # 2 OPERANDS BASE CASE
                if index-1 >= 0 and (isNum(context[index-1]) or WON):   #(dir)
                    e = context[index-1:index+2]    # a op 
                    result = math(e,WON)
                    if result:
                        # if index+2 is in range, chech if context at index+2 is a math_keyword
                        WON = result if index+2 < len(context) and context[index+2] in _math_keywords else None
                        if not WON:
                            result = 'negative '+str(result)[1:] if isNum(result) and numify(result) < 0 else result
                            COMMUNICATION.FORMAT.to_answer(result, audible)

                elif index+3 < len(context):    #(passive)
                    e = context[index:index+4]  # op a div b
                    result = math(e,WON)
                    if result:
                        WON = result if index+4 < len(context) and context[index+4] in _math_keywords else None
                        if not WON:
                            result = 'negative '+str(result)[1:] if isNum(result) and numify(result) < 0 else result
                            COMMUNICATION.FORMAT.to_answer(result, audible)

            ## IsConversion?
            '''elif lowered in _convert_keywords:
                if index-1 or WOKW >= 0:   # inderect?
                    e = context[index-1:index+1]    # a,op
                    result = conversion(e,WON or WOKW)
                    if result:
                        # if index+2 is in range, chech if context at index+2 is a math_keyword
                        if index+1 < len(context):
                            nextkw = context[index+1]
                            if nextkw in _convert_keywords: # if next keyword is a conversion
                                WOKW  = result 
                            elif (numify(result) and nextkw in _math_keywords): # if result is a number and next keyword is mathematical
                                WON = result
                            else:
                                WON = None
                        else:
                            WON = None

                        if not WON:
                            # if result is negative, output is 'negative <result>'
                            result = 'negative '+str(result)[1:] if numify(result) and result < 0 else result
                            COMMUNICATION.FORMAT.to_answer(result, audible)
                    else:
                        COMMUNICATION.FORMAT.to_error('Faulty formula', audible) '''


        elif lowered in ['=','equals','equal','is']:          # Variable Assignment
            variable,value = context[index-1],context[index+1]
            if not variable.isnumeric():
                if value in custom_variables and not value.isnumeric():
                    custom_variables.update({f'{variable}': custom_variables[f'{value}']})
                else:
                    custom_variables.update({f'{variable}': value})
            elif value in custom_variables:
                custom_variables[f'{value}'] = variable
            else:
                COMMUNICATION.FORMAT.to_error(f'Cannot assign {variable} to {value}',audible)

            '''Although we are successfully assigning variables.
               Usage such as x = x+x or a^2 + b^2 = c^2 is faulty'''



        elif lowered in data_keywords['dir_return']:    # Returning Data Queries
            if context[index+1].lower() == 'my':
                request = context[index+2]


                if request.lower() in ['name','username']:
                    COMMUNICATION.FORMAT.normal(f'You are {user}',audible)
                elif request.lower() == 'password':
                    COMMUNICATION.FORMAT.to_special(f'That data is locked',audible)
                else:
                    result = _FRAMEWORK.DATA.get(f'{user}.{request}')
                    if result is not None:
                        request_char = list(request)
                        try:
                            x = request_char.index('_')
                            request_char[x] = ' '
                        except:
                            __excuse__ = None
                        c_request = ''.join(request_char)

                        if isinstance(result,(list,tuple,set)):
                            COMMUNICATION.FORMAT.normal(f'Your {c_request} are {COMMUNICATION.FORMAT.to_group(result, rtn=True, alone=True)}',audible)
                        else:
                            COMMUNICATION.FORMAT.normal(f'Your {c_request} is {result}',audible)
                    else:
                        COMMUNICATION.FORMAT.to_error(f"Seems I don't have that information. Sorry!",audible)

            elif context[index+1].lower() == 'your':
                request = context[index + 2]
                try:
                    info = _FRAMEWORK.DATA.get(f'AI.{request}')
                    COMMUNICATION.FORMAT.normal(info,audible)
                except:
                    COMMUNICATION.FORMAT.normal(f'That information is not found in my database',audible)
            elif _.lower() in ['what is','what does']:
                try:
                    if context[index+2] not in _math_keywords:
                        try:
                            request = context[index + 1]
                            x = custom_variables[request]
                            COMMUNICATION.FORMAT.to_answer(x,audible)
                        except:
                            __excuse__ = None
                except:
                    try:
                        request = context[index + 1]
                        x = custom_variables[request]
                        COMMUNICATION.FORMAT.to_answer(x, audible)
                    except:
                        __excuse__ = None

        elif _.lower() == 'say':
            try:
                COMMUNICATION.FORMAT.normal(" ".join(context[index+1:]), audible)
            except:
                __excuse__ = None

        elif _.lower() in data_keywords['enter_PS']:
            if not personal:
                personal = True
                COMMUNICATION.FORMAT.normal(f"OK, what would you want me to learn?",audible)