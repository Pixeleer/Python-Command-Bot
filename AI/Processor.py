#!/usr/bin/python3
DATABASE,AIAUDIOFILE = 'DATABASE.json','Sarah.mp3'

import COMMUNICATION,FRAMEWORK as _FRAMEWORK, UpdateData
import GROUPING
import json,os,math as _math,time
from random import randint,choice




botaudio, custom_library, grouping = False,False,False

extract = _FRAMEWORK.extract

allowed_context = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y',
                   'z','_',"'",'"'
]
special_characters = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '-', '=', '[', ']', '{', '}', ';',
                      ':','|', ',', '<', '.', '>', '/', '?'
]
math_keywords = {
    'grouping': ['(', ')'],
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
    'dir_return': ['get',"what's",'what is','who is','what are','what does','define', 'what is the','is it'],
    'pas_return': ['can i have','can you tell me'],
    'enter_CL': ['custom', 'custom library','enter custom library', 'open custom library', 'enter custom', 'open custom'],
    'leave_CL': ['exit', 'leave','leave library','exit library', 'leave custom', 'exit custom'],
    'add_to_CL': ['learn','acknowledge', 'add']
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
            if foundAt+1 < len(string) and (keyword == '*' and string[foundAt+1] == '*'):
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

    return toReturn if toReturn != [] else None


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

def tryInt(num):
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
            COMMUNICATION.FORMAT.to_error(f'Could not bring {a} to power',botaudio)'''
            

def custom_processing(context,user):
    global botaudio
    UpdateData.all()

    '''Use of nicknames has been discontinued'''
    #global nickname
    #nickname = _FRAMEWORK.DATA.get(f"{user}.-custom-libray.nickname")

    if context[0] in data_keywords['dir_return']+data_keywords['pas_return']:
        context.pop(0)

    text = ' '.join(context)
    lib = _FRAMEWORK.DATA.get(request=f'{user}.-custom-library')
    if lib:
        find = lib.get(text,None)
        if not find:
            # Find first closest match
            for k,v in lib.items():
                find = k.find(text)
                if find != -1:
                    find = v
                    break
                else:
                    find = None

        if find:
            if isinstance(find, dict):
                X = extract(find, isinstance(find, dict))
                COMMUNICATION.FORMAT.to_group(f"{X}",out=botaudio)
            elif isinstance(find,list):
                X = COMMUNICATION.FORMAT.to_group(find, rtn=True,alone=True)
                COMMUNICATION.FORMAT.normal(f"{X}",out=botaudio)
            else:
                COMMUNICATION.FORMAT.normal(f"{find}",out=botaudio)
            return None
        else:
             COMMUNICATION.FORMAT.normal(f"{text}, is not found in this library", out=botaudio)

def toBinaryOp(eq=[]):
    for i in range(len(eq)):
        _ = eq[i]
        if _ in math_keywords['dir_add']:
            eq[i] = '+'
        elif _ in math_keywords['pas_add']:
            eq[i+2] = '+'
            eq[i] = None
        elif _ in math_keywords['dir_sub']:
            eq[i] = '-'
        elif _ in math_keywords['pas_sub']:
            eq[i+2] = '-'
            eq[i] = None
        elif _ in math_keywords['dir_mult']:
            eq[i] = '*'
        elif _ in math_keywords['pas_mult']:
            eq[i+2] = '*'
            eq[i] = None
        elif _ in math_keywords['dir_div']:
            eq[i] = '/'
        elif _ in math_keywords['pas_div']:
            eq[i+2] = '/'
            eq[i] = None
        elif _ in math_keywords['dir_pow']:
            eq[i] = '^'

    while None in eq:
        eq.remove(None)

    return eq


def process(text,user, allowBotAudio=False,):
    global botaudio,custom_library,adding
    botaudio = allowBotAudio
    if text.lower() in ['shutdown','shut down']:
        return 'shutdown'
    elif text.lower() in ['switch output','switch bot audio']:
        return 'switch output'
    elif text.lower() in ['switch input']:
        return 'switch input'
    elif text.lower() in ['repeat that','repeat','can you repeat that','could you repeat that','please repeat that']:
        os.system(AIAUDIOFILE)
        return
    elif text.lower() in ['sarah','sara']:
        a = ['Yes?','Uh huh?','Mm?','What?','Need something?','Hmm?',f'Yes {user}?']
        COMMUNICATION.FORMAT.normal(choice(a),botaudio)
        return
    elif text.lower() in ['hey','hi','hello','howdy']:
        a = ['Hey!','Hi!','Hello!','Howdy!','Salutations!',f'Hi {user}!']
        COMMUNICATION.FORMAT.normal(choice(a),botaudio)
        return


    context = text if grouping else ContextV4(text) # List of characters split and grouped into keywords, words or numbers
    #print(context) #FOR DEBUG
    if context is None:
        COMMUNICATION.FORMAT.to_error(f"Sorry, I don't understand", botaudio)
        return


    # MATH GROUPING GOES HERE
    
    context_w_equations = GROUPING.getEquations(context, _math_keywords, custom_variables)
    

    # won abbreviates 'Working On Number'
    WON = None
    #WOKW = None


    for index,_ in enumerate(context_w_equations):
        lowered = _.lower() if type(_) is str else '' #Implement this new change#

        # Use Custom Library?
        if custom_library:
            if lowered in data_keywords['leave_CL']:
                custom_library = False
                COMMUNICATION.FORMAT.normal(f"Returning to default library", botaudio)
                return None #Finished
            elif lowered in data_keywords['add_to_CL']:
                '''i = index
                while i < len(context):
                    if context[i] not in ['is', 'equals']:
                        i += 1
                    else:
                        break'''


                # Label_Anser divide
                assign_syntax = -1
                j_context = ' '.join(context)
                try:
                    for case in ['is','equals','=','is equal to','is = to', 'is =']:
                        assign_syntax = case if j_context.find(case) != -1 else -1
                        if assign_syntax != -1:
                            break

                    assert assign_syntax != -1

                    as_i = context.index(assign_syntax)

                    Label = " ".join(context[index + 1:as_i])
                    Value = " ".join(context[as_i+1:])     # Possible out-of-range exepction

                    Value = custom_variables.get(Value,Value)   # Attempt to use Custom variable, else value
                    '''while i < len(context):
                        Value += context[i]
                        i += 1'''
                    
                    print(Value)
                    if Label != '' and Value != '':
                        _FRAMEWORK.DATA.add_data(f'{user}.-custom-library', {Label: Value})
                        COMMUNICATION.FORMAT.normal(f"Given information has been learned", botaudio)
                except:
                    COMMUNICATION.FORMAT.to_error(f"Sorry, I don't understand", botaudio)



                # TODO
                '''if context in del_INFO
                    _FRAMEWORK.DATA.get(f'{user}.-custom-library.{request}')
                '''
            else:
                custom_processing(context,user)

            return  # Quick fix to engage custom library only once       (Solution?)


        ##  IsMath?
        elif type(_) is list:
            groups = GROUPING.GROUP(_)
            for i in range(len(groups)):
                groups[i] = toBinaryOp(groups[i])
            result = GROUPING.dotheting(groups)
            COMMUNICATION.FORMAT.to_answer(result, botaudio)

            ## IsConversion?
        # '''elif lowered in _convert_keywords:
        #     if index-1 or WOKW >= 0:   # inderect?
        #         e = context[index-1:index+1]    # a,op
        #         result = conversion(e,WON or WOKW)
        #         if result:
        #             # if index+2 is in range, chech if context at index+2 is a math_keyword
        #             if index+1 < len(context):
        #                 nextkw = context[index+1]
        #                 if nextkw in _convert_keywords: # if next keyword is a conversion
        #                     WOKW  = result 
        #                 elif (numify(result) and nextkw in _math_keywords): # if result is a number and next keyword is mathematical
        #                     WON = result
        #                 else:
        #                     WON = None
        #             else:
        #                 WON = None

        #             if not WON:
        #                 # if result is negative, output is 'negative <result>'
        #                 result = 'negative '+str(result)[1:] if numify(result) and result < 0 else result
        #                 COMMUNICATION.FORMAT.to_answer(result, botaudio)
        #         else:
        #             COMMUNICATION.FORMAT.to_error('Faulty formula', botaudio) '''
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
                COMMUNICATION.FORMAT.to_error(f'Cannot assign {variable} to {value}',botaudio)

            '''Although we are successfully assigning variables.
               Usage such as x = x+x or a^2 + b^2 = c^2 is faulty'''
        elif lowered in data_keywords['dir_return']:    # Returning Data Queries
            UpdateData.all()
            if not (index+1 < len(context)):
                return

            request = None
            if index+2 < len(context) and context[index+1] == 'my':
                request = context[index+2]
            else:
                request = context[index+1]

            request = request.replace('_',' ')  # for linking multiple worded requests
            
            if request.lower() in ['name','username']:
                COMMUNICATION.FORMAT.normal(f'You are {user}',botaudio)
                return


            keys = _FRAMEWORK.DATA.get(f'{user}').keys()

            if request.lower() in keys:
                value = _FRAMEWORK.DATA.get(f'{user}.{request}')

                if request.lower() == 'password':
                    COMMUNICATION.FORMAT.to_special(f'That data is locked',botaudio)
                else:
                    result = _FRAMEWORK.DATA.get(f'{user}.{request}')
                    if result is not None:
                        request_char = list(request)
                        try:
                            x = request_char.index('_')
                            request_char[x] = ' '
                        except:
                            pass
                        c_request = ''.join(request_char)

                        if isinstance(result,(list,tuple,set)):
                            output = "{}".format(f'Your {c_request} are ' if context[index+1].lower() == 'my' else f'{c_request} are ')
                            COMMUNICATION.FORMAT.normal(
                                output + COMMUNICATION.FORMAT.to_group(result, rtn=True, alone=True),
                                botaudio)
                            pass
                        else:
                            #output = "{}".format(f'Your {a} is ' if a%2 == 0 else 0)
                            output = "{}".format(f'Your {c_request} is ' if context[index+1].lower() == 'my' else f'{c_request} is ') + result
                            COMMUNICATION.FORMAT.normal(output,botaudio)
                    else:
                        COMMUNICATION.FORMAT.to_error(f"Seems I don't have that information. Sorry!",botaudio)

            elif index+2 < len(context) and context[index+1] in ['your', 'AI']:
                request = context[index+2]
                try:
                    info = _FRAMEWORK.DATA.get(f'AI.{request}')
                    COMMUNICATION.FORMAT.normal(info,botaudio)
                except:
                    COMMUNICATION.FORMAT.normal(f'That information is not found in my database',botaudio)
            else:
                try:
                    if context[index+2] not in _math_keywords:
                        try:
                            request = context[index + 1]
                            x = custom_variables[request]
                            COMMUNICATION.FORMAT.to_answer(x,botaudio)
                        except:
                            pass
                except:
                    pass

                try:
                    request = context[index + 1]
                    x = custom_variables[request]
                    COMMUNICATION.FORMAT.to_answer(x, botaudio)
                except:
                    pass

        elif lowered == 'say':
            try:
                COMMUNICATION.FORMAT.normal(" ".join(context[index+1:]), botaudio)
            except:
                pass

        elif lowered in data_keywords['enter_CL']:
            custom_library = True
            COMMUNICATION.FORMAT.normal("I am now linked to your custom library",botaudio)
            return


# test_equations = [
#     '(2^3)'
#     #'( 17 - (6 / 2) ) + 4 * 3',
# ]

# for eq in test_equations:

#     process(eq,'user',False)