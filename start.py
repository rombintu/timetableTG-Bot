# libs
import telebot
import sqlite3
import calendar
# data from libs
from Dates import *
from config import *
from telebot import types
from datetime import datetime, timedelta
from fitcha import *
from random import randint

# FITCHA
def fitcha():
    # length phraseList
    PrasesList_size = len(phrasesList)
    # random number
    nbr = randint(0, PrasesList_size-1)
    return phrasesList[nbr]

# Connect BOT
bot = telebot.TeleBot(TOKEN)

# Global INIT

# BODY
print('Bot is starting...')

# Init message handler
@bot.message_handler(content_types=['text'])
def getCommands(message):
    # get user name
    name = message.from_user.username
    # get user id
    id = message.from_user.id
    # get user request (message)
    req = message.text

    vip = ['eldove', 'nester55', 'angelmuk10', 'NickolskyRoman']
    # commands list
    commands = ['/start', '/news']
    # keyboard-commands list
    kommands = ['Завтра', 'Сегодня', 'Неделя', 'ДЗ']
    keyboard = types.ReplyKeyboardMarkup()

    listDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Назад']
    # NameWeekDayList
    dayList = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # <FUNCTIONS>
    #############
    # func for send message to users from bot
    def print_bot(text):
        bot.send_message(id, text)

    def getWeekNow():
        # Connect DataBase sqlite3
        db = sqlite3.connect("Database.db")
        # create cursor for sql-commands
        sql = db.cursor()
        # open file with data current Week
        sql.execute("SELECT num FROM currentWeek")
        cWeek = sql.fetchone()
        return cWeek[0]


    # set current Week (1 or 0)
    def setWeekNow(currDatetime):
        # Connect DataBase sqlite3
        db = sqlite3.connect("Database.db")
        # create cursor for sql-commands
        sql = db.cursor()
        # just [Var] for set next week
        lastWeek = getWeekNow()
        # var for equals
        nextWeek = lastWeek - 1
        if currDatetime == Dates[nextWeek]:
            newWeek = lastWeek + 1
            sql.execute("UPDATE currentWeek SET num=? WHERE num=?", (newWeek, lastWeek))
            db.commit()

    # func SELECT (sqlite db)
    def select(table):
        # Connect DataBase sqlite3
        db = sqlite3.connect("Database.db")
        # create cursor for sql-commands
        sql = db.cursor()

        # SELECT DATA
        sql.execute('SELECT * FROM "%s"' % table)
        arrAll = sql.fetchall()
        buff = ''
        for elem in arrAll:
            buff += '______________________' + '\n'
            for elem2 in elem:
                buff += '| ' + str(elem2) + '\n'
        print_bot(buff)

        phrase = fitcha()
        print_bot(phrase)


    # Check 0 or 1
    def checkEven():
        weekNow = getWeekNow()
        if weekNow % 2 == 1:
            return True
        else:
            return False

    # func checks NameDay
    def checkDay(date):

        if date == dayList[0]:
            select('mon')
        elif date == dayList[1]:
            if checkEven():
                select('tue1')
            else:
                select('tue2')
        elif date == dayList[2]:
            if checkEven():
                select('wed1')
            else:
                select('wed2')
        elif date == dayList[3]:
            if checkEven():
                select('thu')
            else:
                print_bot('Выходной')
        elif date == dayList[4]:
            if checkEven():
                select('fri1')
            else:
                select('fri2')
        elif date == dayList[5]:
            if checkEven():
                select('sat1')
            else:
                select('sat2')
        elif date == dayList[6]:
            print_bot('Отдыхай, котик')
        else:
            print_bot('К такому жизнь меня не готовила')


    def FuncSelect(day):
        if checkEven():
            select(day + '1')
        else:
            select(day + '2')




    def newsEdit(message):
        text = message.text
        idG = str(text)
        def updateHomeWork(message):
            text = message.text
            homeWork = str(text)
            # Connect DataBase sqlite3
            db = sqlite3.connect("Database.db")
            # create cursor for sql-commands
            sql = db.cursor()
            sql.execute("UPDATE homework SET work=? WHERE id=?", (homeWork, idG))
            db.commit()
            print_bot('Готово')

        print_bot('Напиши изменения')
        bot.register_next_step_handler(message, updateHomeWork)

    ##############
    # </FUNCTIONS>



    # response to commands
    if req == commands[0]:
        # create keyboard one time
        keyboard.row(kommands[0], kommands[1])
        keyboard.row(kommands[3], kommands[2])

        bot.send_message(id, F'Держи клавиатуру {name}, а то запутаешься, дорогой', reply_markup=keyboard)
    elif req == commands[1]:
        if name in vip:
            print_bot('Какой предмет обновить? (id)')
            bot.register_next_step_handler(message, newsEdit)
        else:
            print_bot('У тебя нет права на это действие')
    elif req == kommands[0]:
        # get today
        toDay = datetime.today()
        # get tomorrow
        tomorrow = toDay + timedelta(days=1)
        # format date
        tomorrowStr = tomorrow.strftime("%d.%m.%Y")
        # get Name weekday
        workdate = datetime.strptime(tomorrowStr, '%d.%m.%Y')
        tomorrow_nameWeekDay = calendar.day_abbr[workdate.date().weekday()]
        ##############

        if tomorrow_nameWeekDay == 'Mon':
            setWeekNow(datetime.date(tomorrow))
        ###############

        weekNow = getWeekNow()

        # type phrase
        print_bot(F'Идет {weekNow} неделя\nРасписание на [{tomorrowStr}]')
        # use func
        checkDay(tomorrow_nameWeekDay)

    elif req == kommands[1]:
        # get today datetime
        toDay = datetime.today().strftime("%d.%m.%Y")
        # get Name weekday
        workdate = datetime.strptime(toDay, '%d.%m.%Y')
        ###############
        today_nameWeekDay = calendar.day_abbr[workdate.date().weekday()]

        weekNow = getWeekNow()
        
        # type phrase
        print_bot(F'Идет {weekNow} неделя\nРасписание на [{toDay}]')
        # use func
        checkDay(today_nameWeekDay)


    elif req == kommands[2]:

        keyboard.row(listDays[0], listDays[1], listDays[2])
        keyboard.row(listDays[3], listDays[4], listDays[5])
        keyboard.row(listDays[6])
        bot.send_message(id, 'Выбери день недели', reply_markup=keyboard)

    elif req == kommands[3]:
        select('homework')

    elif req == listDays[0]:
        print_bot('Расписание на понедельник этой недели')
        print_bot('Военка')
    elif req == listDays[1]:
        print_bot('Расписание на вторник этой недели')
        FuncSelect(dayList[1].lower())
    elif req == listDays[2]:
        print_bot('Расписание на среду этой недели')
        FuncSelect(dayList[2].lower())
    elif req == listDays[3]:
        print_bot('Расписание на четверг этой недели')
        if checkEven():
            select('thu')
        else:
            print_bot('Выходной')
    elif req == listDays[4]:
        print_bot('Расписание на пятницу этой недели')
        FuncSelect(dayList[4].lower())
    elif req == listDays[5]:
        print_bot('Расписание на субботу этой недели')
        FuncSelect(dayList[5].lower())
    else:
        # if command not found -> create keyboard
        keyboard.row(kommands[0], kommands[1])
        keyboard.row(kommands[3], kommands[2])
        # get phrase
        phrase = fitcha()
        bot.send_message(id, phrase, reply_markup=keyboard)

# MAIN FUNCTION
if __name__ == '__main__':
    bot.polling(none_stop=True)
