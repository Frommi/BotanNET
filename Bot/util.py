from collections import defaultdict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler
from enum import Enum
import answers

#нужное подставить
cursor = []

#first is group, second is project
#chats_current_place = defaultdict(lambda: ("None", "None"))


class UserType(Enum):
    NO_USER = 0
    USER = 1
    ADMIN = 2



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



def get_user_id(update):
    return update.message.from_user.id


def get_chat_id(update):
    return update.message.chat_id


def too_few_args(bot, chat_id, args, count):
    if len(args) < count:
        bot.send_message(chat_id=chat_id, text=answers.too_few_arguments)
        return None
    return 1


