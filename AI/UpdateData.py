DATABASE = 'DATABASE.JSON'

from AI import FRAMEWORK as _FRAMEWORK
from datetime import datetime
from random import randint
import os,sys,math
from threading import *; from multiprocessing import *
USER = "Creator"

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
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.it morning', new_value='yes')
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.meridiem',new_value='am')
        meridiem = ['am', 'in the morning']
    else:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.it morning', new_value='no')
    if evening:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.it evening', new_value='yes')
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.meridiem', new_value='am')
        meridiem = ['am', 'in the evening']
    else:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.it evening', new_value='no')
    if afternoon:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.it afternoon', new_value='yes')
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.meridiem', new_value='pm')
        meridiem = ['am', 'in the afternoon']
    else:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.it afternoon', new_value='no')
    if night:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.it night', new_value='yes')
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.meridiem', new_value='pm')
        meridiem = ['pm']
    else:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.it night', new_value='no')
    if int(h) > 12:
        h = f"{int(h) - 12}"
    if int(m) == 0:
        m = "o clock"
    elif int(m) < 10:
        m = f'0{m}'
    _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.the time',
                                   new_value="{} : {} {}".format(h, m,meridiem[randint(0,len(meridiem)-1)]))
    _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.what time is it',
                                   new_value="{} : {} {}".format(h, m, meridiem[randint(0, len(meridiem) - 1)]))


def updatedate():
    month_dict = {"1":"January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August",
                  "9":"September","10":"October","11":"November","12":"December"
    }
    m,d,y = datetime.now().month,datetime.now().day,datetime.now().year
    _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.the date',new_value="{} {}, {}".format(month_dict[str(m)],d,y))
    _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.what is today',new_value="{} {}".format(month_dict[str(m)],d))
    _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.what day is it', new_value="{} {}".format(month_dict[str(m)], d))
    _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.the month',new_value=month_dict[str(m)])
    _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.the year',new_value=str(y))

def compinfo():
    cd,cp = current_thread().name,current_process().name
    _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.current thread',new_value=f"{cd}")
    _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.current process', new_value=f"{cp}")
    _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.system flags', new_value=f"{sys.flags}")

def other(): #custom things only
    global nickname
    nickname = _FRAMEWORK.DATA.get(f"{USER}.personal.nickname")
    if nickname in ['nothing ', 'none ', 'off ', 'false ']:
        _FRAMEWORK.DATA.edit_directory(f'{USER}.personal.nickname', new_value=f" ")

def all():
    updatetime()
    updatedate()
    compinfo()
    other()