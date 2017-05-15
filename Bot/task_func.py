import BD
import answers
import re
from telegram.ext import CommandHandler
import util


#args - project_name, task_name
def create_task(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 2) is None:
        return
    names = ("(проекта)", "(таска)")
    for i in range(2):
        if re.fullmatch("\w+", args[i]) is None:
            bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name + names[i])
            return
    try:
        BD.create_task(util.cursor, util.get_user_id(update), args[1], args[0])
    except util.ProjectNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "проект")
    except util.TaskAlreadyExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.already_exists_name % "таск")
    except util.UserIsNotAdmin:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.create_no_admin % "таск")

#args - project_name, task_name
def delete_task(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 2) is None:
        return
    names = ("(проекта)", "(таска)")
    for i in range(2):
        if re.fullmatch("\w+", args[i]) is None:
            bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name + names[i])
            return
    try:
        BD.delete_task(util.cursor, util.get_user_id(update), args[1])#,args[0])
    except util.ProjectNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "проект")
    except util.TaskNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.already_exists_name % "таск")
    except util.UserIsNotAdmin:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.create_no_admin % "таск")

#args - project_name, task_name
def done_task(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 2) is None:
        return
    names = ("(проекта)", "(таска)")
    for i in range(2):
        if re.fullmatch("\w+", args[i]) is None:
            bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name + names[i])
            return
    try:
        BD.set_task(util.cursor, util.get_user_id(update), args[1], True, None)#,args[0])
    except util.ProjectNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "проект")
    except util.TaskNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.already_exists_name % "таск")
    except util.UserHasNotTask:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.create_no_admin % "таск")


#args - project_name, task_name
def undone_task(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 2) is None:
        return
    names = ("(проекта)", "(таска)")
    for i in range(2):
        if re.fullmatch("\w+", args[i]) is None:
            bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name + names[i])
            return
    try:
        BD.set_task(util.cursor, util.get_user_id(update), args[1], False, None)#,args[0])
    except util.ProjectNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "проект")
    except util.TaskNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.already_exists_name % "таск")
    except util.UserHasNotTask:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.create_no_admin % "таск")


#args - project_name, task_name
def hide_task(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 2) is None:
        return
    names = ("(проекта)", "(таска)")
    for i in range(2):
        if re.fullmatch("\w+", args[i]) is None:
            bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name + names[i])
            return
    try:
        BD.set_task(util.cursor, util.get_user_id(update), args[1], None, True)#,args[0])
    except util.ProjectNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "проект")
    except util.TaskNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.already_exists_name % "таск")
    except util.UserHasNotTask:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.create_no_admin % "таск")

#args - project_name, task_name
def unhide_task(bot, update, args):
    if util.too_few_args(bot, util.get_chat_id(update), args, 2) is None:
        return
    names = ("(проекта)", "(таска)")
    for i in range(2):
        if re.fullmatch("\w+", args[i]) is None:
            bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_name + names[i])
            return
    try:
        BD.set_task(util.cursor, util.get_user_id(update), args[1], None, False)#,args[0])
    except util.ProjectNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "проект")
    except util.TaskNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.already_exists_name % "таск")
    except util.UserHasNotTask:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.create_no_admin % "таск")

#task_status d - 'done', u - 'undone'
#args - project_name, task_name1, task_status1, task_name2, task_status2,...
def find_botan(bot, update, args):
    if len(args) % 2 == 0:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_input_tasks)
        return
    for i in range(1, len(args), 2):
        if args[i] != 'u' and args[i] != 'd':
            bot.send_message(chat_id=util.get_chat_id(update), text=answers.incorrect_input_tasks)

    tasks = [(args[i], args[i + 1] == 'd') for i in range(1, len(args), 2)]

    try:
        botans = BD.find_botan(util.cursor, tasks)#,args[0])
        bot.send_message(chat_id=util.get_chat_id(update), text='\n'.join(botans))
    except util.ProjectNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.no_exists_name % "проект")
    except util.TaskNotExistsException:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.already_exists_name % "таск")
    except util.UserHasNotTask:
        bot.send_message(chat_id=util.get_chat_id(update), text=answers.create_no_admin % "таск")


task_handlers = (
    CommandHandler(create_task.__name__, create_task, pass_args=True),
    CommandHandler(delete_task.__name__, delete_task, pass_args=True),
    CommandHandler(done_task.__name__, done_task, pass_args=True),
    CommandHandler(undone_task.__name__, undone_task, pass_args=True),
    CommandHandler(hide_task.__name__, hide_task, pass_args=True),
    CommandHandler(unhide_task.__name__, unhide_task, pass_args=True),
    CommandHandler(find_botan.__name__, find_botan, pass_args=True),
)

# def task_info(bot, update, task_name):
#     pass
