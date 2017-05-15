import BD
import re
import answers
from util import get_chat_id, get_user_id, too_few_args, cursor, \
    GroupNotExistsException, GroupAlreadyExistsException, UserIsNotAdmin
from telegram.ext import CommandHandler


def create_group(bot, update, args):
    if too_few_args(bot, get_chat_id(update), args, 1) is None:
        return

    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        BD.create_group(get_user_id(update), args[0])
    except GroupAlreadyExistsException:
        bot.send_message(chat_id=get_chat_id(update), text=answers.already_exists_name % "группа")


def delete_group(bot, update, args):
    if too_few_args(bot, get_chat_id(update), args, 1) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        BD.delete_group(get_user_id(update), args[0])
    except GroupNotExistsException:
        bot.send_message(chat_id=get_chat_id(update), text=answers.no_exists_name % "группа")
    except UserIsNotAdmin:
        bot.send_message(chat_id=get_chat_id(update), text=answers.delete_no_admin % "группу")

#args - group_name, user_id
def join_user(bot, update, args):
    if too_few_args(bot, get_chat_id(update), args, 2) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        BD.join_user(cursor, args[1], args[0], get_user_id(update))
    except GroupNotExistsException:
        bot.send_message(chat_id=get_chat_id(update), text=answers.no_exists_name % "группа")
    except UserIsNotAdmin:
        bot.send_message(chat_id=get_chat_id(update), text=answers.delete_no_admin % "группу")

#args - group_name, user_id
def unjoin_user(bot, update, args):
    if too_few_args(bot, get_chat_id(update), args, 2) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        BD.unjoin_user(cursor, args[1], args[0], get_user_id(update))
    except GroupNotExistsException:
        bot.send_message(chat_id=get_chat_id(update), text=answers.no_exists_name % "группа")
    except UserIsNotAdmin:
        bot.send_message(chat_id=get_chat_id(update), text=answers.delete_no_admin % "пользователя")

#args - group_name
def enter_group(bot, update, args):
    if too_few_args(bot, get_chat_id(update), args, 1) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        admin_id = BD.get_admin(cursor, args[0])
        bot.send_message(chat_id=admin_id, text="Пожалуйста присоедините меня к " + args[0] + " мой ID: " + get_user_id(update))
    except GroupNotExistsException:
        bot.send_message(chat_id=get_chat_id(update), text=answers.no_exists_name % "группа")

#args - group_name
def exit_group(bot, update, args):
    if too_few_args(bot, get_chat_id(update), args, 1) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        admin_id = BD.get_admin(cursor, args[0])
        BD.unjoin_user(cursor, user_id=get_user_id(update), admin_id=admin_id, group_name= args[0])
        bot.send_message(chat_id=admin_id, text="Человек с ID " + str(get_user_id(update)) + "покинул группу " + args[0])
    except GroupNotExistsException:
        bot.send_message(chat_id=get_chat_id(update), text=answers.no_exists_name % "группа")
    except UserIsNotAdmin:
        bot.send_message(chat_id=get_chat_id(update), text=answers.delete_no_admin % "пользователя")


# def group_info(bot, update, group_name):
#     pass
#
#
# def do_admin(bot, update, user_id):
#     pass
#
#
# def do_user(bot, update, user_id):
#     pass


group_handlers = (
    CommandHandler(create_group.__name__, create_group, pass_args=True),
    CommandHandler(delete_group.__name__, delete_group, pass_args=True),
    CommandHandler(join_user.__name__, join_user, pass_args=True),
    CommandHandler(unjoin_user.__name__, unjoin_user, pass_args=True),
    CommandHandler(enter_group.__name__, enter_group, pass_args=True),
    CommandHandler(exit_group.__name__, exit_group, pass_args=True)
)
