#!/usr/bin/env python
# -*- coding: utf-8 -*-
import basa
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
sub = []
banda = ["367054126", "465166018", "491711894"]


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
        group=int(group)
    )
    html = requests.get(link)
    pars = BeautifulSoup(html.text, "html.parser")
    for paru in pars.find_all(class_="cell mh-50"):
        if paru.text != " ":
            par.append(paru.text)
    for i in par:
        if i != "":
            pardata.append(re.findall("\w+", i))
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
            ret = ret + str(
                str(i + 1) + " пара " + pardata[i][0] + " " + pardata[i][1] + " в аудиторий № " +
                pardata[i][3] + " корпусе " + "№ " + pardata[i][4]) + "\n"
    if len(pardata) >= 7:
        for i in range(len(pardata)):
            if pardata[i][0] == "ЧП":
                ret = "Черговий підрозд1іл"
                break
            ret = ret + str(str(i + 1) + " пара " + pardata[i][0] + " " + pardata[i][1] + " в аудиторий № " + pardata[i][
                3] + " корпусе " + "№ " + pardata[i][4] + " " + "преподователь " + pardata[i][5] + " " + pardata[i][
                   6] + " " + pardata[i][7]) + "\n"
    if pardata == [] and last_chat_text == "вчера":
        ret = 'не было пар'
    elif pardata == [] and last_chat_text == ("завтра" or 'послезавтра'):
        ret = "не будет пар"
    elif pardata == [] and last_chat_text == "сегодня":
        ret = 'нет пар'
    return ret


def generate_markup(items,time, size,):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=time, resize_keyboard=size)
    markup.add(*[types.KeyboardButton(item) for item in items])
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


def simple(mes,group):
    bot.send_message(last_chat_id, last_chat_name + ", " + mes + "\n" + timetable((dayt.index(mes) - 1),group))


dayt = ["вчера", "сегодня", "завтра", "послезавтра"]

mat = ["бля", "сука", "заебался", "надуй", "ебал", "хуйня", "хуй", "пизда"]

new_offset = None
facs=[]
cours=[]
groups=[]

while True:
    try:
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
                    last_chat_text = last_update['message']['text']
                    last_chat_id = last_update['message']['chat']['id']
                    last_chat_name = last_update['message']['chat']['first_name']
                except KeyError:
                    continue
            print(dat)
            if last_chat_text.lower() in mat:
                bot.send_message(last_chat_id, ("Братан, не ссы еще " + str((datetime.datetime(2018, 7, 1) - datetime.datetime.now()).days) + " день"))
            if (last_chat_text == ("/start")) or (last_chat_text == "сменить факультет") or dat.get(str(last_chat_id)) == None :
                if last_chat_text == ("/start"):
                    bot.send_message(last_chat_id,"👋Приветствуем вас, "+str(last_chat_name)+"\nНиже находится клавиатура для управления ботом.\nПриятного пользования!")
                dat[str(last_chat_id)] = ["", "", ""]
                facs = [item for item in basa.basa.keys()]
                bot.send_message(last_chat_id, "выберите факультет:", reply_markup=generate_markup(facs, False, True))
            elif (str(last_chat_text) in facs):
                if (dat.get(str(last_chat_id)) != None):
                    dat[str(last_chat_id)][0] = str(last_chat_text)
                    cours = [item for item in basa.basa[str(dat[str(last_chat_id)][0])].keys()]
                    bot.send_message(last_chat_id, "выберите курс:", reply_markup=generate_markup(cours, False, True))
            elif (str(last_chat_text) in cours):
                if (dat[str(last_chat_id)][0] != ""):
                    dat[str(last_chat_id)][1] = last_chat_text
                    groups = [a for a in basa.basa[str(dat[str(last_chat_id)][0])][dat[str(last_chat_id)][1]]]
                    bot.send_message(last_chat_id, "выберите группу:", reply_markup=generate_markup(groups, False, True))
            elif (str(last_chat_text) in groups):
                if (dat[str(last_chat_id)][1] != ""):
                    dat[str(last_chat_id)][2] = basa.basa_data(str(dat[str(last_chat_id)][0]),
                                                           str(dat[str(last_chat_id)][1]),
                                                           str(last_chat_text))
                    bot.send_message(last_chat_id, "Меню", reply_markup=generate_markup(["сегодня", "вчера", "завтра", "послезавтра", "сменить факультет", "сменить курс", "сменить группу"],
                    False, True, ))
            elif (last_chat_text == "сменить курс") and (str(dat[last_chat_text]) in facs):
                bot.send_message(last_chat_id, "выберите курс:", reply_markup=generate_markup(cours, False, True))
            elif (last_chat_text == "сменить группу") and (str(dat[last_chat_text])[0] in facs) and (str(dat[last_chat_text][1]) in cours):
                bot.send_message(last_chat_id, "выберите группу:", reply_markup=generate_markup(groups, False, True))
            elif (last_chat_text in dayt) and (
                    (str(dat[str(last_chat_id)][0]) in facs) and ((str(dat[str(last_chat_id)][1]) in cours)) and (
                    str(dat[str(last_chat_id)]) != "")):
                simple(last_chat_text, dat[str(last_chat_id)][2])
            else:
                if dat[str(last_chat_id)][0]=="":
                    facs = [item for item in basa.basa.keys()]
                    bot.send_message(last_chat_id, "выберите факультет:",
                                     reply_markup=generate_markup(facs, False, True))
                elif dat[str(last_chat_id)][1]=="":
                    bot.send_message(last_chat_id, "выберите курс:", reply_markup=generate_markup(cours, False, True))
                elif dat[str(last_chat_id)][2]=="":
                    bot.send_message(last_chat_id, "выберите группу:",
                                     reply_markup=generate_markup(groups, False, True))

            new_offset = last_update_id + 1
    except KeyError as err:
        print("Ошибка", err)
        continue