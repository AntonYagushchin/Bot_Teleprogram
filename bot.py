# головний файл бота


import time
from aiogram.utils.markdown import text, bold, italic, code, pre
from datetime import datetime
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from shedule import films_fin, serials_fin, multfilms_fin, multserials_fin
import update_day


#UPDATE BASE
def update_channels():
    update_day.update_all()


def update_all():
    update_channels()
    update_schedules()


def online_schedule(list):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    time = (int(current_time[0:2]) * 60) + int(current_time[3:])
    if list[0][6] < list[0][7]:
        if time < int(list[0][6]):
            return list
        elif time > int(list[0][6]):
            if time > int(list[0][7]):
                return online_schedule(list[1:])
            elif time < int(list[0][6]):
                return list
    elif list[0][6] > list[0][7]:
        if time < 240:
            if time > int(list[0][7]):
                return online_schedule(list[1:])
            elif time < int(list[0][6]):
                return list
        elif time > 240:
            return list

#update_schedules
def update_schedules():

    return films_fin, serials_fin, multfilms_fin, multserials_fin



def update_all():
    update_channels()
    update_schedules()



def make_str_film(sch = online_schedule(films_fin)):
    sch_films_str = ""
    for line in sch:
        l = italic(str(line[0])) + " - " + italic(str(line[1])) + ": " + str(line[2])+ ' ' + ' ' +  str(line[3]) + '\n'
        sch_films_str += l
    return sch_films_str

def make_str_serial(sch = online_schedule(serials_fin)):
    sch_serials_str = ""
    for line in sch:
        l = italic(str(line[0])) + " - " + italic(str(line[1])) + ": " + str(line[2]) + str(line[3]) + '\n'
        sch_serials_str += l
    return sch_serials_str



update_all()

###

sch_films, sch_serials, sch_multfilms, sch_multserials = update_schedules()

###


for line in sch_films:
    line.append('\n')
for line in sch_serials:
    line.append('\n')
for line in sch_multfilms:
    line.append('\n')
for line in sch_multserials:
    line.append('\n')


#Ініціалізація бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

button_films = InlineKeyboardButton('Фільми', callback_data = 'films')
button_serials = InlineKeyboardButton('Серіали', callback_data = 'serial')
button_channel = InlineKeyboardButton('Певний канал', callback_data = 'channel')

kb_choise = InlineKeyboardMarkup().add(button_channel, button_films, button_serials)



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привіт, мене звати Телепрограма_Бот_ЮА і я можу показати тобі список фільмів або серіалів на сьогодні або програму певного телеканалу. Що б ти хотів або хотіла дізнатися?", reply_markup=kb_choise)


@dp.callback_query_handler(lambda c: c.data == 'films')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, str(make_str_film()))


@dp.callback_query_handler(lambda c: c.data == 'serial')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, str(make_str_serial()), parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Допомога")




if __name__ == "__main__":
    executor.start_polling(dp)
    print(sch_films)
    print(sch_films_str)
    print(sch_serials)
    print(sch_serials_str)
