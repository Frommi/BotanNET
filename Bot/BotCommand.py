from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import BD
from group_func import group_handlers
from project_func import project_handlers
from task_func import task_handlers
import util

#from util import chats_current_place, UserType


#TODO: normal start
def start(bot, update):
    chat_id = update.message.chat_id
    try:
        BD.create_user(util.cursor, update.message.from_user.id)
        bot.send_message(chat_id=chat_id, text="Привет, теперь вы с нами, в BotanNET!!")
    except util.UserAlreadyExistsException:
        bot.send_message(chat_id=chat_id, text="Вы уже в BotanNET")


#TODO: normal help and preview
def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="help'а нет, но вы держитесь")



def commit(bot, update):
    util.conn.commit()
    bot.send_message(chat_id=update.message.chat_id, text="Закоммители успешно!")

# def current_place(bot, update):
#     chat_id = update.message.chat_id
#     cur_group, cur_project = chats_current_place[chat_id]
#     bot.send_message(chat_id=update.message.chat_id,
#                      text=answers.current_place % (cur_group, cur_project))
#
#
# def set_current_place(bot, update, args):
#     chat_id = update.message.chat_id
#     try:
#         if BD.user_in(update.message.from_user.id, args[0], args[1]) != UserType.NO_USER:
#             chats_current_place[chat_id] = args[0], args[1]
#         else:
#             bot.send_message(chat_id=chat_id, text=answers.incorrect_set_current_place)
#     except RuntimeError:
#         bot.send_message(chat_id=chat_id, text=answers.incorrect_input)


def quit(bot, update):
    quit_keyboard = [[InlineKeyboardButton("Да", callback_data='Пока'),
                      InlineKeyboardButton("Нет", callback_data='Спасибо, что с нами')]]
    reply_markup = InlineKeyboardMarkup(quit_keyboard)
    update.message.reply_text('Действительно хотите покинуть BotanNet?', reply_markup=reply_markup)


def confim_button(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Ваш выбор: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
    if query == 'Пока':
        BD.delete_user(util.cursor, update.message.from_user.id)


handlers = (
    CommandHandler(start.__name__, start),
    CommandHandler(help.__name__, help),
    CommandHandler(commit.__name__, commit),
    #CommandHandler(current_place.__name__, current_place),
    #CommandHandler(set_current_place.__name__, set_current_place, pass_args=True),
    CommandHandler(quit.__name__, quit),
    CallbackQueryHandler(confim_button),
    *group_handlers, *project_handlers, *task_handlers
)




# BotanNetBot functions:
# /start - начать разговор с ботом
# /help
# /create_group(group_name) - создать группу
#
# /join_to_group(group_name) - отправить запрос на присоединение к существующей
# /quit_group(name_group)
#
# /mark_do((cur_group or group)/(project or cur_project)/task)
# /mark_undo(--||--) => аналогично
#
# /current(cur_project, cur_group) - выставляет текущий проект (cur_group - опциональный аргумент)
#
# /find_who_did(task, project_name)-выводит ссылки на тех, кто сделал
# /find_who_didn't(--||--)
# /quit - закончить разговор с ботом
#
# Для админов:
# /create_project(name)
# /delete_project(name_group, project_name)
#
# /create_task(name)
# /delete_task(name)
#
# /add_user(user_name)
# /delete_user(user_name)
#
# /delete_group(name)
#
#
# Нужные мне функции из работы с базой данных:
#
# Создание/удаления группы
# : user_id, group_name (: передаваемые аргументы)
# возврат факта существования
# : group_name
#
# Создания/удаления проекта
# : group_name, user_id, project_name
# возврата факта существования проекта
# : group_name, project_name
#
# Создание/удаления таск
# : group_name, project_name, task_name, user_id
# возврат факта существования
# : group_name, project_name, task_name, user_id
#
# Отметить таск выполненным/невыполненным/скрытым/открытым
# : group_name, project_name, task_name, user_id, is_did/is_hide
#
# Добавление/удаление user'a(в Users)
# : user_id
#
# Добавления/удаления user'а в группу
# : admin_id, user_id, group_name
#
#
# Найти тех кто сделал/не сделал таск
# : group_name, project_name, is_did
# возвращает list из первых ста