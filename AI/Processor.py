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
    'addition_dir': ['plus','+','combined with','joined with'],
    'addition_pas': ['add','combine','join', 'sum of'],
    'subtraction_dir' : ['minus','-','taken from'],
    'subtraction_pas': ['subtract','take','negate'],
    'multiplication_dir': ['times', '*'],
    'multiplication_pas': ['product of', 'multiple of'],
    'division_dir': ['divided by', '/', 'over'],
    'division_pas': ['quotient of'],
    'powers_dir': ['^', '**','to the power of','to the'],
    'powers_dir_super': ['squared','tripled','quadrupled','turkied']
}
data_keywords = {
    'return_dir': ['get',"what's",'what is','who is','what are','what does'],
    'return_pas': ['can i have','can you tell me'],
    'enter_pm': ['personal setting', 'personal settings','enter personal setting', 'open personal setting'],
    'leave_pm': ['exit','leave setting','exit setting'],
    'enter_add_pm': ['learn','acknowledge']
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
_math_keywords,_data_keywords = group(math_keywords),group(data_keywords)
def check_fkw(string):
    string = str(string.lower())
    string_chars = list(string)
    ignore_dict = {}
    diff,loop,last_index = 0,0,None

    while loop < len(string):
        for keyword in _math_keywords+_data_keywords:
            to_find = keyword.lower()
            _from = string.find(to_find)
            if to_find in ignore_dict:
                _from = string.find(to_find, ignore_dict[to_find], len(string))
            if _from != -1:
                ignore_dict.update({f'{keyword}': _from + len(keyword)})
                step = _from + len(keyword) - 1
                if len(keyword) > 0:
                    if last_index is None or _from > last_index:
                        last_index = _from
                        while step > _from:
                            string_chars.pop(step - diff)
                            step -= 1
                        string_chars[step - diff] = to_find

                    elif _from < last_index:
                        last_index = _from
                        while step > _from:
                            string_chars.pop(step)
                            step -= 1
                        string_chars[step] = to_find
                    diff = diff + len(to_find) - 1
                else:
                    string_chars[_from] = to_find
        loop += 1

    return string_chars
def ContextV3(text):
    text_array = check_fkw(text)
    if text_array is None:
        return None
    a = list()
    build = None

    for i,_ in enumerate(text_array):
        if _ == " ":
            if build is not None:
                a.append(build)
                build = None
            continue
        if build is None and _.isnumeric(): # start build with number number character
            build = _
        elif build is None and not _.isnumeric(): # start build with letter character
            build = _
        elif (build[-1].isnumeric() or build[-1] == '.') and _.isnumeric(): # add number character to build if build is number
            build += _
        elif not build.isnumeric() and not _.isnumeric():# add letter character to build if build is letter
            build += _
        elif build.isnumeric() and not _.isnumeric():
            if _ == '.':
                build += _
            else:
                a.append(build)
                build = _
        elif not build.isnumeric() and _.isnumeric():
            a.append(build)
            build = _

    if build is not None:
        a.append(build)

    return a
def math(action,context,index,x=None):
    def numify(num):
        try:
            return int(num)
        except:
            return float(num)

    def round(num):
        try:
            if isinstance(num,float):
                nl = list(str(num))
                while nl[-3] != '.':
                    nl.pop(-1)
                return "".join(nl)
            else:
                return num
        except:
            return num

    if action == math_keywords['addition_dir']:
        _one,_two = x or context[index-1], context[index+1]
        if _one in custom_variables:
            _one = custom_variables[_one]
        if _two in custom_variables:
            _two = custom_variables[_two]

        try:
            x,y = numify(_one),numify(_two)
            return round(x+y)
        except:
            try:
                x = _one + _two
                return round(x)
            except:
                COMMUNICATION.FORMAT.to_error(f'Unable to add {_one} and {_two}',True)
    if action == math_keywords['addition_pas']:
        _one, _two = x or context[index + 1], context[index + 3]
        if _one in custom_variables:
            _one = custom_variables[_one]
        if _two in custom_variables:
            _two = custom_variables[_two]
        try:
            x, y = numify(_one), numify(_two)
            return round(x+y)
        except:
            try:
                x = _one + _two
                return round(x)
            except:
                COMMUNICATION.FORMAT.to_error(f'Unable to add {_one} and {_two}', True)

    if action == math_keywords['subtraction_dir']:
        _one, _two = x or context[index - 1], context[index + 1]
        if _one in custom_variables:
            _one = custom_variables[_one]
        if _two in custom_variables:
            _two = custom_variables[_two]
        try:
            x, y = numify(_one), numify(_two)
            if context[index] == 'taken from':
                return round(y-x)
            else:
                return round(x-y)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to subtract {_one} and {_two}', True)

    if action == math_keywords['subtraction_pas']:
        _one,_two = x or context[index+1],context[index+3]
        if _one in custom_variables:
            _one = custom_variables[_one]
        if _two in custom_variables:
            _two = custom_variables[_two]

        try:
            x,y = numify(_one),numify(_two)
            if context[index] == 'from':
                return round(y-x)
            else:
                return round(x-y)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to subtract {_one} and {_two}',True)
    if action == math_keywords['multiplication_dir']:
        _one, _two = x or context[index - 1], context[index + 1]
        if _one in custom_variables:
            _one = custom_variables[_one]
        if _two in custom_variables:
            _two = custom_variables[_two]

        try:
            x, y = numify(_one), numify(_two)
            return round(x*y)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to multiply {_one} and {_two}', True)

    if action == math_keywords['multiplication_pas']:
        _one,_two = x or context[index+1],context[index+3]
        if _one in custom_variables:
            _one = custom_variables[_one]
        if _two in custom_variables:
            _two = custom_variables[_two]

        try:
            x, y = numify(_one), numify(_two)
            return round(x*y)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to multiply {_one} and {_two}', True)

    if action == math_keywords['division_dir']:
        _one, _two = x or context[index - 1], context[index + 1]
        if _one in custom_variables:
            _one = custom_variables[_one]
        if _two in custom_variables:
            _two = custom_variables[_two]

        try:
            x, y = numify(_one), numify(_two)
            return round(x/y)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to divide {_one} and {_two}', audible)

    if action == math_keywords['division_pas']:
        _one,_two = x or context[index+1],context[index+3]
        if _one in custom_variables:
            _one = custom_variables[_one]
        if _two in custom_variables:
            _two = custom_variables[_two]

        try:
            x, y = numify(_one), numify(_two)
            return round(x/y)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to divide {_one} and {_two}', audible)

    if action == math_keywords['powers_dir']:
        _one, _two = x or context[index - 1], context[index + 1]
        if _one in custom_variables:
            _one = custom_variables[_one]
        if _two in custom_variables:
            _two = custom_variables[_two]

        if _one == 'power':
            _one = context[index - 2]
        try:
            x, y = numify(_one), numify(_two)
            return round(x**y)
        except:
            COMMUNICATION.FORMAT.to_error(f'Unable to bring {_one} to the power of {_two}', audible)

    if action == math_keywords['powers_dir_super']:
        _num,_format = x or context[index-1], context[index]
        if _num in custom_variables:
            _num = custom_variables[_num]

        try:
            _num = numify(_num)
            if _format == 'squared':
                return round(_num**2)
            elif _format == 'tripled':
                return round(_num**3)
            elif _format == 'quadrupled':
                return round(_num**4)
            elif _format == 'turkied':
                return round(_num**5)
        except:
            COMMUNICATION.FORMAT.to_error(f'Could not bring {_num} to power',audible)
def personal_processing(text,user='Creator'):
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
        a = ['yes?','uh huh?','mm?','what?','need something?','hmm?',f'yes {user}']
        COMMUNICATION.FORMAT.normal(choice(a),audible)
        return
    elif text.lower() in ['hey','hi','hello','howdy']:
        a = ['hey!','hi!','hello!','howdy!','salutations!',f'hi {user}']
        COMMUNICATION.FORMAT.normal(choice(a),audible)
        return
    global personal,adding


    context = ContextV3(text)

    if context is None:
        COMMUNICATION.FORMAT.to_error(f"There was an error comprehending some of your words i'm afraid", audible)
        return
    if personal:
        for index,_ in enumerate(context):
            if _.lower() in data_keywords['leave_pm']:
                personal = False
                COMMUNICATION.FORMAT.normal(f"I'm now assigned to normal settings", audible)
                return None #Finished
            elif _.lower() in data_keywords['enter_add_pm']:
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
            personal_processing(text,user)
        adding = False
        return None  # Finished
    group_return = list()

    # won abbreviates 'Working On Number'
    won = None
    for index,_ in enumerate(context):
        if _.lower() in math_keywords['addition_dir']:
            result = math(math_keywords['addition_dir'],context,index,won)
            if result is not None:
                try:
                    if context[index+2] in _math_keywords:
                        won = result
                    else:
                        won = None
                        COMMUNICATION.FORMAT.to_answer(result, audible)
                except:
                    COMMUNICATION.FORMAT.to_answer(result, audible)
        if _.lower() in math_keywords['addition_pas']:
            result = math(math_keywords['addition_pas'], context, index, won)
            if result is not None:
                try:
                    if context[index+4] in _math_keywords:
                        won = result
                    else:
                        won = None
                        COMMUNICATION.FORMAT.to_answer(result, audible)
                except:
                    COMMUNICATION.FORMAT.to_answer(result, audible)
        if _.lower() in math_keywords['subtraction_dir']:
            result = math(math_keywords['subtraction_dir'], context, index, won)
            if result is not None:
                try:
                    if context[index + 2] in _math_keywords:
                        won = result
                    else:
                        won = None
                        COMMUNICATION.FORMAT.to_answer(result, audible)
                except:
                    COMMUNICATION.FORMAT.to_answer(result, audible_output)
        if _.lower() in math_keywords['subtraction_pas']:
            result = math(math_keywords['subtraction_pas'], context, index, won)
            if result is not None:
                try:
                    if context[index + 4] in _math_keywords:
                        won = result
                    else:
                        won = None
                        COMMUNICATION.FORMAT.to_answer(result, audible)
                except:
                    COMMUNICATION.FORMAT.to_answer(result, audible_output)
        if _.lower() in math_keywords['multiplication_dir']:
            result = math(math_keywords['multiplication_dir'], context, index, won)
            if result is not None:
                try:
                    if context[index + 2] in _math_keywords:
                        won = result
                    else:
                        won = None
                        COMMUNICATION.FORMAT.to_answer(result, audible)
                except:
                    COMMUNICATION.FORMAT.to_answer(result, audible)
        if _.lower() in math_keywords['multiplication_pas']:
            result = math(math_keywords['multiplication_pas'], context, index, won)
            if result is not None:
                try:
                    if context[index + 4] in _math_keywords:
                        won = result
                    else:
                        won = None
                        COMMUNICATION.FORMAT.to_answer(result, audible)
                except:
                    COMMUNICATION.FORMAT.to_answer(result, audible)
        if _.lower() in math_keywords['division_dir']:
            result = math(math_keywords['division_dir'], context, index, won)
            if result is not None:
                try:
                    if context[index + 2] in _math_keywords:
                        won = result
                    else:
                        won = None
                        COMMUNICATION.FORMAT.to_answer(result, audible)
                except:
                    COMMUNICATION.FORMAT.to_answer(result, audible)
        if _.lower() in math_keywords['division_pas']:
            result = math(math_keywords['division_pas'], context, index, won)
            if result is not None:
                try:
                    if context[index + 4] in _math_keywords:
                        won = result
                    else:
                        won = None
                        COMMUNICATION.FORMAT.to_answer(result, audible)
                except:
                    COMMUNICATION.FORMAT.to_answer(result, audible)
        if _.lower() in math_keywords['powers_dir']:
            result = math(math_keywords['powers_dir'], context, index, won)
            if result is not None:
                try:
                    if context[index + 2] in _math_keywords:
                        won = result
                    else:
                        won = None
                        COMMUNICATION.FORMAT.to_answer(result, audible)
                except:
                    COMMUNICATION.FORMAT.to_answer(result, audible)
        if _.lower() in math_keywords['powers_dir_super']:
            result = math(math_keywords['powers_dir_super'], context, index, won)
            if result is not None:
                try:
                    if context[index + 1] in _math_keywords:
                        won = result
                    else:
                        won = None
                        COMMUNICATION.FORMAT.to_answer(result, audible)
                except:
                    COMMUNICATION.FORMAT.to_answer(result, audible)

        if _.lower() in ['=','equals','equal','is']:
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


        if _.lower() in data_keywords['return_dir']:
            if context[index+1].lower() == 'my':
                request = context[index+2]
                if request.lower() == 'personal': # Personal is private so we don't give info
                    COMMUNICATION.FORMAT.to_special(f'That data is locked',audible)
                    return None
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
                            COMMUNICATION.FORMAT.normal(x,audible)
                        except:
                            __excuse__ = None
                except:
                    try:
                        request = context[index + 1]
                        x = custom_variables[request]
                        COMMUNICATION.FORMAT.normal(x, audible)
                    except:
                        __excuse__ = None

                    # Although we are successfully assigning variables.
                    # Usage such as x = x+x or a^2 + b^2 = c^2 is faulty
        if _.lower() == 'say':
            try:
                COMMUNICATION.FORMAT.normal(" ".join(context[index+1:]), audible)
            except:
                __excuse__ = None

        if _.lower() in data_keywords['enter_pm']:
            if not personal:
                personal = True
                COMMUNICATION.FORMAT.normal(f"I'm now assigned to your personal settings",audible)