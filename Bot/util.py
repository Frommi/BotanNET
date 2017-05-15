from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler
import answers
import psycopg2

#нужное подставить
cursor = None
conn = None


class BotanException(Exception):
    pass


class ElemNotExistsException(BotanException):
    pass

class UserNotExistsException(ElemNotExistsException):
    pass

class GroupNotExistsException(ElemNotExistsException):
    pass

class ProjectNotExistsException(ElemNotExistsException):
    pass

class TaskNotExistsException(ElemNotExistsException):
    pass


class ElemAlreadyExistsException(BotanException):
    pass

class UserAlreadyExistsException(ElemAlreadyExistsException):
    pass

class GroupAlreadyExistsException(ElemAlreadyExistsException):
    pass

class ProjectAlreadyExistsException(ElemAlreadyExistsException):
    pass

class TaskAlreadyExistsException(ElemAlreadyExistsException):
    pass

class UserHasNotTask(BotanException):
    pass

class UserIsNotAdmin(BotanException):
    pass

def init_BD():
    global cursor, conn

    conn_string = "host='localhost' dbname='botannet' user='postgres' password='secret'"
    print("Connecting to database\n ->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("Connected!")

def get_user_id(update):
    return update.message.from_user.id


def get_chat_id(update):
    return update.message.chat_id


def too_few_args(bot, chat_id, args, count):
    if len(args) < count:
        bot.send_message(chat_id=chat_id, text=answers.too_few_arguments)
        return None
    return 1


