import BD
import answers
import re
from util import get_chat_id, get_user_id, too_few_args, cursor, \
    GroupNotExistsException, ProjectNotExistsException, ProjectAlreadyExistsException, UserIsNotAdmin
from telegram.ext import CommandHandler

#args - group_name, project_name
def create_project(bot, update, args):
    if too_few_args(bot, get_chat_id(update), args, 2) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=get_chat_id(update), text=answers.incorrect_name + "(группы)")
        return
    if re.fullmatch("\w+", args[1]) is None:
        bot.send_message(chat_id=get_chat_id(update), text=answers.incorrect_name + "(проекта)")
        return
    try:
        BD.create_project(cursor, get_user_id(update), args[0], args[1])
    except ProjectAlreadyExistsException:
        bot.send_message(chat_id=get_chat_id(update), ext=answers.already_exists_name % "проект")
    except UserIsNotAdmin:
        bot.send_message(chat_id=get_chat_id(update), text=answers.create_no_admin % "проект")

#args = project_name
def delete_project(bot, update, args):
    if too_few_args(bot, get_chat_id(update), args, 1) is None:
        return
    if re.fullmatch("\w+", args[0]) is None:
        bot.send_message(chat_id=get_chat_id(update), text=answers.incorrect_name + "(проекта)")
        return
    try:
        BD.delete_project(cursor, get_user_id(update), args[0])
    except ProjectNotExistsException:
        bot.send_message(chat_id=get_chat_id(update),text=answers.no_exists_name % "проект")
    except UserIsNotAdmin:
        bot.send_message(chat_id=get_chat_id(update),text=answers.delete_no_admin % "проект")

# def project_info(bot, update, user_id, string_name):
#     pass

project_handlers = (
    CommandHandler(create_project.__name__, create_project, pass_args=True),
    CommandHandler(delete_project.__name__, delete_project, pass_args=True)
)



