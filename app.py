import requests
import datetime
from bs4 import BeautifulSoup
import re
import telebot
from telebot import types

token = "560289646:AAFzO2loYla3rOfMPBT_1S9YihU1JYN6dBU"
api_url = "https://api.telegram.org/bot{}/".format(token)
bot = telebot.TeleBot(token)
markup = types.ReplyKeyboardMarkup()
dat = {}
sub=[]


def vdata(d=0):
    nowdata = datetime.datetime.now() + datetime.timedelta(days=d)
    if nowdata.day < 10 and nowdata.month < 10:
        data = str("0" + str(nowdata.day) + ".0" + str(nowdata.month) + "." + str(nowdata.year))
    elif nowdata.day > 10 and nowdata.month < 10:
        data = str(str(nowdata.day) + ".0" + str(nowdata.month) + "." + str(nowdata.year))
    elif nowdata.day < 10 and nowdata.month > 10:
        data = str("0" + str(nowdata.day) + "." + str(nowdata.month) + "." + str(nowdata.year))
    else:
        data = str(str(nowdata.day) + "." + str(nowdata.month) + "." + str(nowdata.year))
    return data


def timetable(d=0, group=257):
    data = vdata(d)
    ret = ''
    pardata = []
    par = []
    link = "http://rozklad.univd.edu.ua/timeTable/group?TimeTableForm%5Bfaculty%5D=4&TimeTableForm%5Bcourse%5D=&TimeTableForm%5Bgroup%5D={group}&TimeTableForm%5Bdate1%5D={data}&TimeTableForm%5Bdate2%5D={data}&TimeTableForm%5Br11%5D=5&timeTable=0".format(
        data=data,
        group=group
    )
    print(link)
    html = requests.get(link)
    pars = BeautifulSoup(html.text, "html.parser")
    for paru in pars.find_all(class_="cell mh-50"):
        if paru.text != " ":
            par.append(paru.text)
    for i in par:
        if i != "":
            pardata.append(re.findall("\w+", i))
    print(pardata)
    for i in pardata:
        if i[2] != "ауд":
            i[0] = i[0] + "-" + i[1]
            i.remove(i[1])
        if i[3] == "тир":
            i.insert(4, "-")
        if i[3] == "спорт":
            i.insert(4, "-")
    if len(pardata) < 7:
        for i in range(len(pardata)):
            ret = ret + str(str(i + 1) + " пара " + pardata[i][0] + " " + pardata[i][1] + " в аудиторий № " + pardata[i][3] + " корпусе " + "№ " + pardata[i][4]) + "\n"
    if len(pardata) >= 7:
        for i in range(len(pardata)):
            if pardata[i][0] == "ЧП":
                ret = "Черговий підрозд1іл"
                break
            ret = ret + str( str(i + 1) + " пара " + pardata[i][0] + " " + pardata[i][1] + " в аудиторий № " + pardata[i][3] + " корпусе " + "№ " + pardata[i][4] + " " + "преподователь " + pardata[i][5] + " " + pardata[i][6] + " " + pardata[i][7]) + "\n"
    if pardata == []:
        ret = ' нету пар'

    return ret


def generate_markup(items, time, size):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=time, resize_keyboard=size)
    markup.add(*[types.KeyboardButton(item) for item in items])
    markup.add("меню")
    return markup


def get_last_update():
    get_result = get_updates()
    if len(get_result) > 0:
        last_update = get_result[-1]
    else:
        last_update = None
    return last_update



def get_updates(offset=None, timeout=100):
    method = 'getUpdates'
    params = {'timeout': timeout, 'offset': offset}
    resp = requests.get(api_url + method, params)
    result_json = resp.json()['result']
    return result_json


def simple(mes):
    bot.send_message(last_chat_id, last_chat_name +", "+mes +"\n" + timetable((dayt.index(mes) - 1), grouplist[str(dat[str(last_chat_id)][1])]))

def data(c=0,g=0):
    if c == []:
        g=dat[str(last_chat_id)][0]
    if c == []:
        g =dat[str(last_chat_id)][1]
    return [c,g]
course=["1","2","4"]
grouplist = {"101" : 258, "102" : 257, "201" : 63, "202" : 64 , "401" : 65 , "402" : 66, "403": 67, "404": 68}
dayt = ["вчера", "сегодня", "завтра", "послезавтра"]
new_offset = None
while True:

    if get_updates(new_offset) == []:
        get_updates(None)
    else:
        get_updates(new_offset)
    if get_last_update() == None:
        continue
    else:
        try:
            last_update = get_last_update()
            last_update_id = last_update['update_id']
            last_chat_text = str(last_update['message']['text'])
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']
        except KeyError:
            continue
    if last_chat_text.lower() == "заебался":
        bot.send_message(last_chat_id, ("Братан, не ссы еще " + str(
            (datetime.datetime(2018, 7, 1) - datetime.datetime.now()).days) + " день"))
    if last_chat_text == ("/start") or last_chat_text == "сменить курс" or (str(last_chat_id) not in dat):
        dat[str(last_chat_id)]=[[],[]]
        bot.send_message(last_chat_id, "выберите курс:", reply_markup=generate_markup(["1", "2", "4"], False, True))
    elif (last_chat_text in dayt):
        simple(last_chat_text)
    elif (last_chat_text in course) or ((str(dat[str(last_chat_id)][0]) in course) and last_chat_text=="сменить группу"):
        if last_chat_text =="1" or dat[str(last_chat_id)][0]=="1":
            bot.send_message(last_chat_id, "выберите группу:",reply_markup=generate_markup(["101","102"], False, True))
            dat[str(last_chat_id)][0]="1"
        elif last_chat_text =="2" or dat[str(last_chat_id)][0]=="2":
            bot.send_message(last_chat_id, "выберите группу:",reply_markup=generate_markup(["201","202"], False, True))
            dat[str(last_chat_id)][0]="2"
        elif last_chat_text =="4" or dat[str(last_chat_id)][0]=="4":
            bot.send_message(last_chat_id, "выберите группу:",
                             reply_markup=generate_markup(["401", "402", "403", "404"], False, True))
            dat[str(last_chat_id)][0]="4"
    elif (last_chat_text in grouplist) or (last_chat_text=="меню" and (str(dat[str(last_chat_id)][0]) in course and str(dat[str(last_chat_id)][0]) in grouplist)):
        dat[str(last_chat_id)][1] = last_chat_text
        bot.send_message(last_chat_id, "Меню", reply_markup=generate_markup(
            ["завтра", "послезавтра", "сегодня", "вчера", "сменить курс", "сменить группу"], False, True))
    else:
        if (str(dat[str(last_chat_id)][0]) not in course):
            dat[str(last_chat_id)] = [[], []]
            bot.send_message(last_chat_id, "выберите курс:", reply_markup=generate_markup(["1", "2", "4"], False, True))
        elif (str(dat[str(last_chat_id)][0]) in course) and (str(dat[str(last_chat_id)][1]) not in grouplist):
            if dat[str(last_chat_id)][0] == "1":
                bot.send_message(last_chat_id, "выберите группу:", reply_markup=generate_markup(["101","102"], False, True))
            elif dat[str(last_chat_id)][0] == "2":
                bot.send_message(last_chat_id, "выберите группу:", reply_markup=generate_markup(["201", "202"], False, True))
            elif dat[str(last_chat_id)][0] == "4" :
                bot.send_message(last_chat_id, "выберите группу:", reply_markup=generate_markup(["401","402","403","404"], False, True))
        elif (str(dat[str(last_chat_id)][0]) in course) and (str(dat[str(last_chat_id)][1]) in grouplist):
            bot.send_message(last_chat_id, "Меню", reply_markup=generate_markup(["завтра", "послезавтра", "сегодня", "вчера", "сменить курс", "сменить группу"], False, True))
        else:
            dat[str(last_chat_id)] = [[], []]
            bot.send_message(last_chat_id, "выберите курс:", reply_markup=generate_markup(["1", "2", "4"], False, True))

    new_offset = last_update_id + 1
