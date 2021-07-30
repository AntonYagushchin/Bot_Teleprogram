#В цьому файлі формуються списки фільмів та серіалів, які потім будуть оброблятися файлом бота та виводитись користувачу


import sqlite3 as sq
from operator import itemgetter
import time

dict_of_link = {
    '"Inter"': "https://teleprograma.com.ua/channels/1489/",
    '"Україна"': "https://teleprograma.com.ua/channels/1463/",
    '"СТБ"': "https://teleprograma.com.ua/channels/1506/",
    '"Новий канал"': "https://tvgid.ua/channels/noviy_kanal/",#тут інше посилання, порібна окрема функція
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
mass_of_names = dict_of_link.keys()
#print(mass_of_names)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sq.Error as e:
        print(f"The error '{e}' occurred")


schedule_1 = []
schedule_2 = []

def make_sch_films1_new():
    films = []
    serials = []
    multserials = []
    multfilms = []
    with sq.connect('base.db') as con:
        for name in mass_of_names:
            sql = """SELECT * FROM {}""".format(name)
            cortaige = execute_read_query(con,sql)
            i = 0
            for line in cortaige:
                temp = []
                if line[2] == 'film' and line[3] == 1:
                    for elem in cortaige[i]:
                        temp.append(elem)
                    try:
                        temp.insert(1, cortaige[i+1][0])
                    except IndexError:
                        temp.insert(1, '25:00')#v kinechnome var. vivoditi zmist 25:00 znak pitannya
                    temp.insert(3, name)
                    films.append(temp)
                    i+=1
                elif line[2] == 'serial' and line[3] == 1:
                    for elem in cortaige[i]:
                        temp.append(elem)
                    try:
                        temp.insert(1, cortaige[i + 1][0])
                    except IndexError:
                        temp.insert(1, '25:00')#v kinechnome var. vivoditi zmist 25:00 znak pitannya
                    temp.insert(3, name)
                    serials.append(temp)
                    i += 1
                elif line[2] == 'multserial' and line[3] == 1:
                    for elem in cortaige[i]:
                        temp.append(elem)
                    try:
                        temp.insert(1, cortaige[i+1][0])
                    except IndexError:
                        temp.insert(1, '25:00')#v kinechnome var. vivoditi zmist 25:00 znak pitannya
                    temp.insert(3, name)
                    multserials.append(temp)
                    i+=1
                elif line[2] == "multfilm" and line[3] == 1:
                    for elem in cortaige[i]:
                        temp.append(elem)
                    try:
                        temp.insert(1, cortaige[i+1][0])
                    except IndexError:
                        temp.insert(1, '25:00')#v kinechnome var. vivoditi zmist 25:00 znak pitannya
                    temp.insert(3, name)
                    multfilms.append(temp)
                    i+=1
                elif line[2] == 'notype':
                    i+=1

    for i in range(len(films)):
        hours = int(films[i][0][0:2])
        minutes = int(films[i][0][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        films[i].append(fin)
    for i in range(len(films)):
        hours = int(films[i][1][0:2])
        minutes = int(films[i][1][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        films[i].append(fin)
    films = sorted(films, key=itemgetter(6))
    for i in range(len(films)):
        s = films[i][2]
        # print(s)
        s = s.replace("\xa0", '')
        # print(s)
        films[i][2] = s


    for i in range(len(serials)):
        hours = int(serials[i][0][0:2])
        minutes = int(serials[i][0][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        serials[i].append(fin)
    for i in range(len(serials)):
        hours = int(serials[i][1][0:2])
        minutes = int(serials[i][1][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        serials[i].append(fin)
    serials = sorted(serials, key=itemgetter(6))
    for i in range(len(serials)):
        s = serials[i][2]
        # print(s)
        s = s.replace("\xa0", '')
        # print(s)
        serials[i][2] = s



    for i in range(len(multfilms)):
        hours = int(multfilms[i][0][0:2])
        minutes = int(multfilms[i][0][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        multfilms[i].append(fin)
    for i in range(len(multfilms)):
        hours = int(multfilms[i][1][0:2])
        minutes = int(multfilms[i][1][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        multfilms[i].append(fin)
    multfilms = sorted(multfilms, key=itemgetter(6))
    for i in range(len(multfilms)):
        s = multfilms[i][2]
        # print(s)
        s = s.replace("\xa0", '')
        # print(s)
        multfilms[i][2] = s


    for i in range(len(multserials)):
        hours = int(multserials[i][0][0:2])
        minutes = int(multserials[i][0][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        multserials[i].append(fin)
    for i in range(len(multserials)):
        hours = int(multserials[i][1][0:2])
        minutes = int(multserials[i][1][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        multserials[i].append(fin)
    multserials = sorted(multserials, key=itemgetter(6))
    for i in range(len(multserials)):
        s = multserials[i][2]
        # print(s)
        s = s.replace("\xa0", '')
        # print(s)
        multserials[i][2] = s


    return films, serials, multfilms, multserials

def make_sch_films2_new():
    films = []
    serials = []
    multserials = []
    multfilms = []
    with sq.connect('base.db') as con:
        for name in mass_of_names:
            sql = """SELECT * FROM {}""".format(name)
            cortaige = execute_read_query(con, sql)
            print(cortaige)
            i = 0
            for line in cortaige:
                temp = []
                if line[2] == 'film' and line[3] == 2:
                    for elem in cortaige[i]:
                        temp.append(elem)
                    try:
                        temp.insert(1, cortaige[i+1][0])
                    except IndexError:
                        temp.insert(1, '25:00')#v kinechnome var. vivoditi zmist 25:00 znak pitannya
                    temp.insert(3, name)
                    films.append(temp)
                    i+=1
                elif line[2] == 'serial' and line[3] == 2:
                    for elem in cortaige[i]:
                        temp.append(elem)
                    try:
                        temp.insert(1, cortaige[i + 1][0])
                    except IndexError:
                        temp.insert(1, '25:00')#v kinechnome var. vivoditi zmist 25:00 znak pitannya
                    temp.insert(3, name)
                    serials.append(temp)
                    i += 1
                elif line[2] == 'multserial' and line[3] == 2:
                    for elem in cortaige[i]:
                        temp.append(elem)
                    try:
                        temp.insert(1, cortaige[i+1][0])
                    except IndexError:
                        temp.insert(1, '25:00')#v kinechnome var. vivoditi zmist 25:00 znak pitannya
                    temp.insert(3, name)
                    multserials.append(temp)
                    i+=1
                elif line[2] == "multfilm" and line[3] == 2:
                    for elem in cortaige[i]:
                        temp.append(elem)
                    try:
                        temp.insert(1, cortaige[i+1][0])
                    except IndexError:
                        temp.insert(1, '25:00')#v kinechnome var. vivoditi zmist 25:00 znak pitannya
                    temp.insert(3, name)
                    multfilms.append(temp)
                    i+=1
                elif line[2] == 'notype':
                    i+=1

    for i in range(len(films)):
        hours = int(films[i][0][0:2])
        minutes = int(films[i][0][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        films[i].append(fin)
    for i in range(len(films)):
        hours = int(films[i][1][0:2])
        minutes = int(films[i][1][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        films[i].append(fin)
    films = sorted(films, key=itemgetter(6))
    for i in range(len(films)):
        s = films[i][2]
        # print(s)
        s = s.replace("\xa0", '')
        # print(s)
        films[i][2] = s


    for i in range(len(serials)):
        hours = int(serials[i][0][0:2])
        minutes = int(serials[i][0][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        serials[i].append(fin)
    for i in range(len(serials)):
        hours = int(serials[i][1][0:2])
        minutes = int(serials[i][1][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        serials[i].append(fin)
    serials = sorted(serials, key=itemgetter(6))
    for i in range(len(serials)):
        s = serials[i][2]
        # print(s)
        s = s.replace("\xa0", '')
        # print(s)
        serials[i][2] = s



    for i in range(len(multfilms)):
        hours = int(multfilms[i][0][0:2])
        minutes = int(multfilms[i][0][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        multfilms[i].append(fin)
    for i in range(len(multfilms)):
        hours = int(multfilms[i][1][0:2])
        minutes = int(multfilms[i][1][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        multfilms[i].append(fin)
    multfilms = sorted(multfilms, key=itemgetter(6))
    for i in range(len(multfilms)):
        s = multfilms[i][2]
        # print(s)
        s = s.replace("\xa0", '')
        # print(s)
        multfilms[i][2] = s


    for i in range(len(multserials)):
        hours = int(multserials[i][0][0:2])
        minutes = int(multserials[i][0][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        multserials[i].append(fin)
    for i in range(len(multserials)):
        hours = int(multserials[i][1][0:2])
        minutes = int(multserials[i][1][3:5])
        # print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        multserials[i].append(fin)
    multserials = sorted(multserials, key=itemgetter(6))
    for i in range(len(multserials)):
        s = multserials[i][2]
        # print(s)
        s = s.replace("\xa0", '')
        # print(s)
        multserials[i][2] = s


    return films, serials, multfilms, multserials

def make_schedule_films_1():
    with sq.connect("base.db") as con:
        for name in mass_of_names:
            sql = """SELECT time,name FROM {} WHERE type = 'film' AND list_type = 1;""".format(name)
            cortaige = execute_read_query(con, sql)
            if len(cortaige) > 0:
                for a in cortaige:
                    a = list(a)
                    a.append(name)
                    schedule_1.append(a)
    #print(schedule_1)
    for i in range(len(schedule_1)):
        s = schedule_1[i][1]
        #print(s)
        s = s.replace("\xa0", '')
        #print(s)
        schedule_1[i][1] = s

    for i in range(len(schedule_1)):
        hours = int(schedule_1[i][0][0:2])
        minutes = int(schedule_1[i][0][3:5])
        #print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        schedule_1[i].append(fin)
    schedule_1_sorted = sorted(schedule_1, key=itemgetter(3))
    return schedule_1_sorted



def make_schedule_films_2():
    with sq.connect("base.db") as con:
        for name in mass_of_names:

            sql = """SELECT time,name FROM {} WHERE type = 'film' AND list_type = 2;""".format(name)
            cortaige = execute_read_query(con, sql)
            if len(cortaige) > 0:
                for a in cortaige:
                    a = list(a)
                    a.append(name)
                    schedule_2.append(a)
    #print(schedule_2)
    for i in range(len(schedule_2)):
        s = schedule_2[i][1]
        #print(s)
        s = s.replace("\xa0", '')
        #print(s)
        schedule_2[i][1] = s

    for i in range(len(schedule_2)):
        hours = int(schedule_2[i][0][0:2])
        minutes = int(schedule_2[i][0][3:5])
        #print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        schedule_2[i].append(fin)
    schedule_2_sorted = sorted(schedule_2, key=itemgetter(3))
    return schedule_2_sorted


#schedule_type_1 = make_schedule_films_1()
#print(schedule_type_1)
#schedule_type_2 = make_schedule_films_2()

#print(schedule_type_2)
#schedule_final = schedule_type_1 + schedule_type_2
#print(schedule_final)




#SERIALS


schedule_1_s = []
schedule_2_s = []


def make_schedule_serials_1():
    with sq.connect("base.db") as con:
        for name in mass_of_names:

            sql = """SELECT time,name FROM {} WHERE type = 'serial' AND list_type = 1;""".format(name)
            cortaige = execute_read_query(con, sql)
            if len(cortaige) > 0:
                for a in cortaige:
                    a = list(a)
                    a.append(name)
                    schedule_1_s.append(a)
    #print(schedule_1_s)
    for i in range(len(schedule_1_s)):
        s = schedule_1_s[i][1]
        #print(s)
        s = s.replace("\xa0", '')
        #print(s)
        schedule_1_s[i][1] = s

    #print(schedule_1_s)

    for i in range(len(schedule_1_s)):
        hours = int(schedule_1_s[i][0][0:2])
        minutes = int(schedule_1_s[i][0][3:5])
        #print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        schedule_1_s[i].append(fin)
    schedule_1_s_sorted = sorted(schedule_1_s, key=itemgetter(3))
    return schedule_1_s_sorted



def make_schedule_serials_2():
    with sq.connect("base.db") as con:
        for name in mass_of_names:

            sql = """SELECT time,name FROM {} WHERE type = 'serial' AND list_type = 2;""".format(name)
            cortaige = execute_read_query(con, sql)
            if len(cortaige) > 0:
                for a in cortaige:
                    a = list(a)
                    a.append(name)
                    schedule_2_s.append(a)
    #print(schedule_2_s)
    for i in range(len(schedule_2_s)):
        s = schedule_2_s[i][1]
        #print(s)
        s = s.replace("\xa0", '')
        #print(s)
        schedule_2_s[i][1] = s


    for i in range(len(schedule_2_s)):
        hours = int(schedule_2_s[i][0][0:2])
        minutes = int(schedule_2_s[i][0][3:5])
        #print(hours, minutes)
        fin = int(hours) * 60 + int(minutes)
        schedule_2_s[i].append(fin)
    schedule_2_s_sorted = sorted(schedule_2_s, key=itemgetter(3))
    return schedule_2_s_sorted


#schedule_final_serials = make_schedule_serials_1() + make_schedule_serials_2()
#print(schedule_final_serials)

films1, serials1, multfilms1, multserials1 = make_sch_films1_new()
films2, serials2, multfilms2, multserials2 = make_sch_films2_new()

films_fin = films1 + films2
serials_fin = serials1 + serials2
multfilms_fin = multfilms1 + multfilms2
multserials_fin = multserials1 + multserials2
print(films_fin)
