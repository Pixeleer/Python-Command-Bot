#!/usr/bin/python3
DATABASE = 'DATABASE.JSON'

import FRAMEWORK as _FRAMEWORK
from datetime import datetime
from random import randint
import os,sys,math
from threading import *; from multiprocessing import *
USER = None

def updatetime():
    global meridiem
    h, m = datetime.now().hour, datetime.now().minute
    morning,evening,afternoon,night = False,False,False,False
    if h>= 0 and h < 5:
        night = True
    elif h >= 5 and h <= 9: # is evening
        evening = True
    elif h > 9 and h < 12: # is morning
        morning = True
    elif h >= 12 and h < 18: # is afternoon
        afternoon = True
    elif h >= 18 and h < 24: # is night
        night = True

    if morning:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.morning', new_value='yes')
        _FRAMEWORK.DATA.edit_directory(f'{USER}.meridiem',new_value='am')
        meridiem = ['am', 'in the morning']
    else:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.morning', new_value='no')
    if evening:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.evening', new_value='yes')
        _FRAMEWORK.DATA.edit_directory(f'{USER}.meridiem', new_value='am')
        meridiem = ['am', 'in the evening']
    else:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.evening', new_value='no')
    if afternoon:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.afternoon', new_value='yes')
        _FRAMEWORK.DATA.edit_directory(f'{USER}.meridiem', new_value='pm')
        meridiem = ['am', 'in the afternoon']
    else:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.afternoon', new_value='no')
    if night:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.night', new_value='yes')
        _FRAMEWORK.DATA.edit_directory(f'{USER}.meridiem', new_value='pm')
        meridiem = ['pm']
    else:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.night', new_value='no')
    if int(h) > 12:
        h = f"{int(h) - 12}"
    if int(m) == 0:
        m = "o clock"
    elif int(m) < 10:
        m = f'0{m}'
    _FRAMEWORK.DATA.edit_directory(f'{USER}.time',
                                   new_value="{} : {} {}".format(h, m,meridiem[randint(0,len(meridiem)-1)]))
    '''_FRAMEWORK.DATA.edit_directory(f'{USER}.what time is it',
                                   new_value="{} : {} {}".format(h, m, meridiem[randint(0, len(meridiem) - 1)]))'''


def updatedate():
    month_dict = {"1":"January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August",
                  "9":"September","10":"October","11":"November","12":"December"
    }
    m,d,y = datetime.now().month,datetime.now().day,datetime.now().year
    _FRAMEWORK.DATA.edit_directory(f'{USER}.date',new_value="{} {}, {}".format(month_dict[str(m)],d,y))
    _FRAMEWORK.DATA.edit_directory(f'{USER}.today',new_value="{} {}".format(month_dict[str(m)],d))
    _FRAMEWORK.DATA.edit_directory(f'{USER}.day', new_value="{} {}".format(month_dict[str(m)], d))
    _FRAMEWORK.DATA.edit_directory(f'{USER}.month',new_value=month_dict[str(m)])
    _FRAMEWORK.DATA.edit_directory(f'{USER}.year',new_value=str(y))

def compinfo():
    ct,cp = current_thread().name,current_process().name
    _FRAMEWORK.DATA.edit_directory(f'{USER}.thread',new_value=f"{ct}")
    _FRAMEWORK.DATA.edit_directory(f'{USER}.process', new_value=f"{cp}")
    _FRAMEWORK.DATA.edit_directory(f'{USER}.system flags', new_value=f"{(sys.flags)}".split(','))


# Discontinued
'''def other(): #custom things only
    global nickname
    nickname = _FRAMEWORK.DATA.get(f"{USER}.nickname")
    if nickname in ['nothing ', 'none ', 'off ', 'false ']:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.nickname', new_value=f" ")'''

def all():
    updatetime()
    updatedate()
    compinfo()
    #other()