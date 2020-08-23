import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot("1356720716:AAH71ksKD-dr1R3gdfr4wZ1D3l_7A_cZ9Ek")

print("Bot starting...")

@bot.message_handler(content_types=["text"])
def getTextMessages(message):
    db = sqlite3.connect("database.db")
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS users (id INT, bal INT)""")
    db.commit()
    markup = types.ReplyKeyboardMarkup()
    userID = message.from_user.id
    mess = message.text
    commands = ["/start", "Баланс", "Добавить", "Убавить", "Обнулить"]

    class user():
        id = ''
        bal = 0

        def __init__(self, id, bal):
            self.id = id
            self.bal = bal

        def getBal(self):
            return self.bal

    if mess == commands[0]:
        sql.execute("SELECT id FROM users WHERE id='%s'" % userID)
        if sql.fetchone() is None:
            bot.send_message(userID, "Твой ID: " + str(userID))
            newUser = user(userID, 0)
            sql.execute("INSERT INTO users VALUES(?,?)", (newUser.id, newUser.bal))
            db.commit()
            bot.send_message(userID, "Новый пользователь создан")
        else:
            bot.send_message(userID, "Вы уже зарегистрированы, " + str(message.from_user.first_name))
        db.close()
    elif mess == commands[1]:
        sql.execute("SELECT bal FROM users WHERE id='%s'" % userID)
        balance = sql.fetchone()
        bot.send_message(userID, "Твой баланс: " + str(balance[0]))
    elif mess == commands[2]:
        def addCoin(message):
            val = message.text
            userIDnow = int(message.from_user.id)
            try:
                val = int(val)
                if val > 0:
                    db = sqlite3.connect("database.db")
                    sql = db.cursor()
                    sql.execute("SELECT bal FROM users WHERE id='%s'" % userID)
                    listBal = sql.fetchone()
                    balUser = int(listBal[0])
                    newBalance = balUser + val
                    sql.execute("UPDATE users SET bal=? WHERE id=?", (newBalance, userIDnow))
                    db.commit()
                    db.close()
                    bot.send_message(userIDnow, "Готово, " + str(message.from_user.first_name))
                else:
                    bot.send_message(userIDnow, "Ожидается положительное число")
            except ValueError:
                bot.send_message(userIDnow, "Ожидается число")
        bot.send_message(userID, "Напишите сумму")
        bot.register_next_step_handler(message, addCoin)
    elif mess == commands[3]:
        def delCoin(message):
            val = message.text
            userIDnow = message.from_user.id
            try:
                val = int(val)
                if val > 0:
                    db = sqlite3.connect("database.db")
                    sql = db.cursor()
                    sql.execute("SELECT bal FROM users WHERE id='%s'" % userIDnow)
                    listBal = sql.fetchone()
                    balUser = int(listBal[0])
                    newBalance = balUser - val
                    if newBalance < 0:
                        sql.execute("UPDATE users SET bal=? WHERE id=?", (0, userIDnow))
                        db.commit()
                        db.close()
                    else:
                        sql.execute("UPDATE users SET bal=? WHERE id=?", (newBalance, userIDnow))
                        db.commit()
                        db.close()
                    bot.send_message(message.from_user.id, "Готово, " + str(message.from_user.first_name))
                else:
                    bot.send_message(message.from_user.id, "Ожидается положительное число")
            except ValueError:
                bot.send_message(message.from_user.id, "Ожидается число")

        bot.send_message(userID, "Напишите сумму")
        bot.register_next_step_handler(message, delCoin)
    elif mess == commands[4]:
        db = sqlite3.connect("database.db")
        sql = db.cursor()
        sql.execute("UPDATE users SET bal=? WHERE id=?", (0, userID))
        db.commit()
        db.close()
        bot.send_message(userID, "Готово, " + str(message.from_user.first_name))
    elif mess == "Привет" or mess == "привет":
        bot.send_message(userID, "Привет, " + str(message.from_user.first_name))
    else:
        bot.send_message(userID, "Команда не найдена")
        sql.execute("SELECT id FROM users WHERE id='%s'" % userID)
        if sql.fetchone() is None:
            bot.send_message(userID, "Воспользуйтесь командой /start")

        markup.row(commands[4], commands[1])
        markup.row(commands[3], commands[2])
        bot.send_message(userID, "Выбери команду", reply_markup=markup)

if __name__ == '__main__':
    bot.polling(none_stop=True)
