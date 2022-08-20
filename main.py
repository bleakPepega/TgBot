import telebot
import sqlite3
from threading import Lock
from telebot import types  # для указание типов

bot = telebot.TeleBot("")
connect = sqlite3.connect("tasks", check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                                        numberTheme STRING, 
                                        task STRING,
                                        right_answer STRING
                                    )
                                                   """)
connect.commit()
mutex = Lock()
listForTask = []
#
# cursor.execute("SELECT * FROM tasks")
# all_results = cursor.fetchall()
# print(all_results[1][1])
# print(all_results)


@bot.message_handler(commands=["AddTest"])
def addTest(message):
    bot.send_message(message.chat.id, "Выберите раздел или тему")
    test = message.text.split()
    print(test)

    @bot.message_handler(commands=['razdel'])
    def add_number_theme(message1):
        listForTask.append(message1.text.split())
        print(message1.text.split())
        bot.send_message(message1.chat.id, "Введите задания ")

    @bot.message_handler(commands=['razdel2'])
    def add_task(message2):
        listForTask.append(message2.text.split())

    @bot.message_handler(commands=['razdel3'])
    def add_right_answer(message3):
        bot.send_message(message3.chat.id, "Введите номера ответов ")
        listForTask.append(message3.text.split())

    @bot.message_handler(commands=["push"])
    def acept_changes(message4):
        try:
            try:
                mutex.acquire()
                print(listForTask)
                update_list_for_task = [listForTask[0][0], listForTask[1][0], listForTask[2][0]]
                cursor.execute("INSERT INTO tasks VALUES(?, ?, ?);", update_list_for_task)
                print("its worked")
                connect.commit()
            finally:
                mutex.release()
        except sqlite3.IntegrityError:
            pass
        listForTask.clear()


@bot.message_handler(commands=["choose"])
def choose_theme(message):
    cursor.execute("SELECT * FROM tasks")
    all_results = cursor.fetchall()
    theme = ""
    task = ""
    rightAnswer = ""
    for i in range(len(all_results)):
        theme += all_results[i][0]
        theme += " "
        task += all_results[i][1]
        task += " "
        rightAnswer += all_results[i][2]
        rightAnswer += " "
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, "выберете тему \n")
    bot.send_message(message.chat.id, theme)

    @bot.message_handler(content_types=['text'])
    def answer_on_theme(message1):
        for j in range(len(all_results)):
            print(message1)
            print(all_results[i][0])
            if message1.text == all_results[i][0]:
                print("ayaya")
                bot.send_message(message.chat.id, task[i][0])


# def main():
bot.polling()
