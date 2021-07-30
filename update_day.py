# Парсер та зв'язок з БД

import sqlite3
import sqlite3 as sq
import requests
from bs4 import BeautifulSoup
import lxml
import fake_useragent

###CONSTANTS
user = fake_useragent.UserAgent().random
header = {'user-agent': user}
###CONSTANTS



def clear_ch(name):
    sql_create = """CREATE TABLE {0} (time TEXT, name TEXT, type TEXT, list_type INTEGER)""".format(str(name))
    sql_drop = """DROP TABLE {0}""".format(str(name))

    try:
        with sq.connect("base.db") as con:
            cur = con.cursor()
            cur.execute(sql_create)
    except sqlite3.OperationalError:
        with sq.connect("base.db") as con:
            cur = con.cursor()
            cur.execute(sql_drop)
            cur.execute(sql_create)

def update_films():
    response = requests.get(headers=header).text
    soup = BeautifulSoup(response, "lxml")
    block = soup.find("div", {"class": "row last-film-block"})
    with sq.connect("base.db") as con:
        for container_of_channel in block.find_all("div", {"class": "col-sm-6"}):
            for p in container_of_channel.find_all("p"):
                channel = p.find("a").text
                time = p.find("strong").text
                p = p.text
                p = p.replace(channel, "")
                p = p.replace(time, "")
                data_tuple = (channel, p, time)
                insert = """INSERT INTO films (channel, name, time, list_type) VALUES (?, ?, ?, ?);"""
                con.execute(insert, data_tuple)


dict_of_link = {
    '"Inter"': "https://teleprograma.com.ua/channels/1489/",
    '"Україна"': "https://teleprograma.com.ua/channels/1463/",
    '"СТБ"': "https://teleprograma.com.ua/channels/1506/",
    '"ICTV"': "https://teleprograma.com.ua/channels/1502/",
    '"1+1"': "https://teleprograma.com.ua/channels/1480/",
    '"2+2"': "https://teleprograma.com.ua/channels/1468/",
    '"НТН"': "https://teleprograma.com.ua/channels/1467/",
    '"ТЕТ"': "https://teleprograma.com.ua/channels/1559/",
    '"НЛО TV"': "https://teleprograma.com.ua/channels/1532/",
    '"К1"': "https://teleprograma.com.ua/channels/1465/",
    '"К2"': "https://teleprograma.com.ua/channels/1466/",
    '"Мега"': "https://teleprograma.com.ua/channels/1469/",
    '"UA:Перший"': "https://teleprograma.com.ua/channels/1505/",
    '"Сонце"': "https://teleprograma.com.ua/channels/1535/",
    '"Бігуді"': "https://teleprograma.com.ua/channels/1500/",
    '"УНІАН ТБ"': "https://teleprograma.com.ua/channels/1521/",
    '"Індиго"': "https://teleprograma.com.ua/channels/1456/",
    '"Enter-фільм"': "https://teleprograma.com.ua/channels/1547/",
    '"Еспресо TV"': "https://teleprograma.com.ua/channels/1552/",
    '"Перший автомобільний"': "https://teleprograma.com.ua/channels/1493/",
    '"5 канал"': "https://teleprograma.com.ua/channels/1462/",
    '"Zoom"': "https://teleprograma.com.ua/channels/1484/",
    '"Малятко TV"': "https://teleprograma.com.ua/channels/1507/",
    '"ПлюсПлюс"': "https://teleprograma.com.ua/channels/1470/",
    '"Піксель"': "https://teleprograma.com.ua/channels/1472/",
}

def update_new_channel():
    link = "https://tvgid.ua/channels/noviy_kanal/"

    #Так як у цьому каналі не відображаються х\ф і м\с, візьмемо з іншого сайту

    clear_ch("'Новий канал'")
    response = requests.get(link, headers=header).content
    soup = BeautifulSoup(response, "lxml")
    block = soup.find("table", id="container")
    list = []
    i = 0
    for a in block.find_all("td", class_="time"):
        list.append([])
        list[i].append(a.text)
        i += 1
    j = 0
    for e in block.find_all("td", class_="item"):
        list[j].append(e.text)
        if "Х/ф" in e.text:
            list[j].append("film")
        elif "Т/с" in e.text:
            list[j].append("serial")
        elif "М/с" in e.text:
            list[j].append("multserial")
        elif "М/ф" in e.text:
            list[j].append("multfilm")
        else:
            list[j].append("notype")
        j += 1
    max_time = 0
    list_flag = 1
    for i in range(len(list)):
        hours = list[i][0][0:2]
        minutes = list[i][0][3:5]
        #print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        if max_time < fin:
            max_time = fin
        elif max_time > fin:
            list_flag = 2
        list[i].append(list_flag)

    with sq.connect("base.db") as con:
        for elem in list:
            tuple_temp = (elem[0], elem[1], elem[2], elem[3])
            insert = """INSERT INTO 'Новий канал' (time, name, type, list_type) VALUES (?, ?, ?, ?);"""
            con.execute(insert, tuple_temp)



def update_all():
    update_new_channel()
    mass_of_names = dict_of_link.keys()
    #print(mass_of_names)
    for name in mass_of_names:
        update_channel(name=name, link = dict_of_link[name])



def update_channel(name, link):
    clear_ch(name)
    response = requests.get(link, headers=header).text
    soup = BeautifulSoup(response, "lxml")
    block = soup.find("div", class_="b-tv-channel-schedule__items")
    list = []
    i=0
    for a in block.find_all("span", class_="tv-event__time_single"):
        list.append([])
        list[i].append(a.text)
        i += 1
    j = 0
    for e in block.find_all("div", class_="tv-event__title"):
        list[j].append(e.text)
        if "Х/ф" in e.text:
            list[j].append("film")
        elif "Т/с" in e.text:
            list[j].append("serial")
        elif "М/с" in e.text:
            list[j].append("multserial")
        elif "М/ф" in e.text:
            list[j].append("multfilm")
        else:
            list[j].append("notype")
        j += 1
    max_time = 0
    list_flag = 1
    for i in range(len(list)):
        hours = list[i][0][0:2]
        minutes = list[i][0][3:5]
        #print(hours, minutes)
        fin = int(hours)*60 + int(minutes)
        if max_time < fin:
            max_time = fin
        elif max_time > fin:
            list_flag = 2
        list[i].append(list_flag)


    with sq.connect("base.db") as con:
        for elem in list:
            tuple_temp = (elem[0], elem[1], elem[2], elem[3])
            insert = """INSERT INTO """+name+""" (time, name, type, list_type) VALUES (?, ?, ?, ?);"""
            con.execute(insert, tuple_temp)


update_all()