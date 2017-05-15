import BD
import re
import answers
import util
from telegram.ext import CommandHandler


def create_group(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 1) is None:
        return

    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        print("cursor = ", util.cursor)
        BD.create_group(util.cursor, util.get_user_id(update), args[0])
    except util.GroupAlreadyExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.already_exists_name % "группа")


def delete_group(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 1) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        BD.delete_group(util.cursor, util.get_user_id(update), args[0])
    except util.GroupNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "группа")
    except util.UserIsNotAdmin:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.delete_no_admin % "группу")

#args - group_name, user_id
def join_user(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 2) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        BD.join_user(util.cursor, args[1], args[0], util.get_user_id(update))
    except util.GroupNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "группа")
    except util.UserIsNotAdmin:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.delete_no_admin % "группу")

#args - group_name, user_id
def unjoin_user(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 2) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        BD.unjoin_user(util.cursor, args[1], args[0], util.get_user_id(update))
    except util.GroupNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "группа")
    except util.UserIsNotAdmin:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.delete_no_admin % "пользователя")

#args - group_name
def enter_group(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 1) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        admin_id = BD.get_admin(util.cursor, args[0])
        bot.send_message(chat_id=admin_id, text="Пожалуйста присоедините меня к " + args[0] + " мой ID: " + util.get_user_id(update))
    except util.GroupNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "группа")

#args - group_name
def exit_group(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 1) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name)
        return
    try:
        admin_id = BD.get_admin(util.cursor, args[0])
        BD.unjoin_user(util.cursor, user_id=util.get_user_id(update), admin_id=admin_id, group_name= args[0])
        bot.send_message(chat_id=admin_id, text="Человек с ID " + str(util.get_user_id(update)) + "покинул группу " + args[0])
    except util.GroupNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "группа")
    except util.UserIsNotAdmin:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.delete_no_admin % "пользователя")


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
