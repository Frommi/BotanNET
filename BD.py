from collections import defaultdict
from enum import Enum

chats_current_place = defaultdict(lambda: ("None", "None"))


class UserType(Enum):
    NO_USER = 0
    USER = 1
    ADMIN = 2


class BotanException(Exception):
    pass


class GroupExistsError(BotanException):
    pass


class UserIsNotAdmin(BotanException):
    pass

#поднимает GroupExistsError, если группа с таким именем существует
def create_group(user_id, group_name):
    pass

#поднимает GroupExistsError, если группа с таким именем не существует или UserIsNotAdmin
def delete_group(user_id, group_name):
    pass


#возвращает UserType
def user_in(user_id, group_name, project_name):
    pass


def create_project(user_id, project_name, group_name):
    pass


def delete_project(user_id, project_name, group_name):
    pass


def create_task(user_id, task_name, project_name, group_name):
    pass


def delete_task(user_id, task_name, project_name, group_name):
    pass


#task_done and task_hide - это булевские переменные
#В случае если какая-нибудь из них равна None, значение этой переменнной изменять не требуется


def set_task(user_id, task_name, task_done, task_hide, project_name, group_name):
    pass


def create_user(user_id):
    pass


def delete_user(user_id):
    pass


def join_user(user_id, group_name):
    pass


def unjoin_user(user_id, group_name):
    pass


#возвращает list из первых ста
#tasks - list из кортежей (task_id, и значение должно быть сделанным или не сделанным)
def find_same(tasks):
    pass

