import BD
import answers
import re
import util
from telegram.ext import CommandHandler

#args - group_name, project_name
def create_project(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 2) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name + "(группы)")
        return
    if re.fullmatch("\w+", args[1]) is None:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name + "(проекта)")
        return
    try:
        BD.create_project(util.cursor, util.get_user_id(update), args[1], args[0])
    except util.ProjectAlreadyExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), ext=answers.already_exists_name % "проект")
    except util.UserIsNotAdmin:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.create_no_admin % "проект")

#args = project_name
def delete_project(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 1) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name + "(проекта)")
        return
    try:
        BD.delete_project(util.cursor, util.get_user_id(update), args[0])
    except util.ProjectNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update),text=answers.no_exists_name % "проект")
    except util.UserIsNotAdmin:
        bot.send_message(chat_id=util.get_chat_id(update),text=answers.delete_no_admin % "проект")

# def project_info(bot, update, user_id, string_name):
#     pass

project_handlers = (
    CommandHandler(create_project.__name__, create_project, pass_args=True),
    CommandHandler(delete_project.__name__, delete_project, pass_args=True)
)



