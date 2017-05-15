from util import *

def has_user(cursor, user_id):
    cursor.execute("""SELECT user_id FROM users WHERE user_id = %s;""", [user_id])
    records = cursor.fetchall()
    return bool(records)

def get_group_id(cursor, group_name):
    cursor.execute("""SELECT group_id FROM groups WHERE group_name = %s;""", [group_name])
    records = cursor.fetchall()
    if records:
        return records[0]
    return None

def get_project_id(cursor, project_name):
    cursor.execute("""SELECT project_id FROM projects WHERE project_name = %s;""", [project_name])
    records = cursor.fetchall()
    if records:
        return records[0]
    return None

def get_task_id(cursor, task_info):
    cursor.execute("""SELECT task_id FROM tasks WHERE task_info = %s;""", [task_info])
    records = cursor.fetchall()
    if records:
        return records[0]
    return None

def is_admin(cursor, user_id, group_id):
    cursor.execute("""SELECT is_admin FROM user_groups WHERE user_id = %s AND group_id = %s;""", [user_id, group_id])
    records = cursor.fetchall()
    if records is None:
        return False
    return records[0]


def create_user(cursor, user_id):
    if has_user(cursor, user_id):
        raise UserAlreadyExistsException()

    cursor.execute("""INSERT INTO users VALUES (%s);""", [user_id])

def delete_user(cursor, user_id):
    if not has_user(cursor, user_id):
        raise UserNotExistsException()

    cursor.execute("""DELETE FROM users       WHERE user_id = %s;""", [user_id])
    cursor.execute("""DELETE FROM user_groups WHERE user_id = %s;""", [user_id])
    cursor.execute("""DELETE FROM user_tasks  WHERE user_id = %s;""", [user_id])


def create_group(cursor, user_id, group_name, group_info=None):
    if get_group_id(cursor, group_name) is not None:
        raise GroupAlreadyExistsException()

    cursor.execute("""INSERT INTO groups VALUES (DEFAULT, %s, %s) RETURNING group_id;""", [group_name, group_info])
    group_id = cursor.fetchone()[0]

    cursor.execute("""INSERT INTO user_groups VALUES (%s, %s, %s);""", [group_id, user_id, True])

def delete_group(cursor, user_id, group_name):
    group_id = get_group_id(cursor, group_name)
    if group_id is None:
        raise GroupNotExistsException()

    cursor.execute("""DELETE FROM groups      WHERE group_id = %s;""", [group_id])
    cursor.execute("""DELETE FROM projects    WHERE group_id = %s;""", [group_id])
    cursor.execute("""DELETE FROM user_groups WHERE group_id = %s;""", [group_id])


def create_project(cursor, user_id, project_name, group_name, project_info=None):
    if get_project_id(cursor, project_name) is not None:
        raise ProjectAlreadyExistsException()

    group_id = get_group_id(cursor, group_name)
    if group_id is None:
        raise GroupNotExistsException()

    cursor.execute("""INSERT INTO projects VALUES (DEFAULT, %s, %s, %s);""",
        [project_name, group_id, project_info])

def delete_project(cursor, user_id, project_name):
    project_id = get_project_id(cursor, project_name)
    if project_id is None:
        raise ProjectNotExistsException()

    cursor.execute("""DELETE FROM projects WHERE project_id = %s;""", [project_id])


def create_task(cursor, user_id, task_info, project_name):
    if get_task_id(cursor, task_info) is not None:
        raise TaskAlreadyExistsException()

    project_id = get_project_id(cursor, project_name)
    if project_id is None:
        raise ProjectNotExistsException()

    cursor.execute("""INSERT INTO tasks VALUES (DEFAULT, %s, %s);""", [task_info, project_id])

def delete_task(cursor, user_id, task_info):
    task_id = get_task_id(cursor, task_info)
    if task_id is None:
        raise TaskNotExistsException()

    cursor.execute("""DELETE FROM tasks         WHERE task_id = %s;""", [task_id])
    cursor.execute("""DELETE FROM user_tasks    WHERE task_id = %s;""", [task_id])


def join_user(cursor, user_id, group_name, admin_id):
    group_id = get_group_id(cursor, group_name)
    if group_id is None:
        raise GroupNotExistsException()

    if admin_id is not None:
        if not is_admin(cursor, admin_id, group_id):
            raise UserIsNotAdmin()

    cursor.execute("""INSERT INTO user_groups VALUES (%s, %s, %s);""", [group_id, user_id, False])

def unjoin_user(cursor, user_id, group_name, admin_id):
    group_id = get_group_id(cursor, group_name)
    if group_id is None:
        raise GroupNotExistsException()

    if admin_id is not None:
        if not is_admin(cursor, admin_id, group_id):
            raise UserIsNotAdmin()

    cursor.execute("""DELETE FROM user_groups WHERE user_id = %s AND group_id = %s;""", [user_id, group_id])


#task_done and task_hide - это булевские переменные
#В случае если какая-нибудь из них равна None, значение этой переменнной изменять не требуется
def set_task(cursor, user_id, task_info, task_done, task_hide):
    task_id = get_task_id(cursor, task_info)
    if task_id is None:
        raise TaskNotExistsException()

    cursor.execute("""DELETE FROM user_tasks WHERE user_id = %s AND task_id = %s;""", [user_id, task_id])
    cursor.execute("""INSERT INTO user_tasks VALUES (%s, %s, %s, %s);""", [user_id, task_id, task_hide, task_done])


#возвращает list из первых ста
#tasks - list из кортежей (task_id, task_must be done)
def find_botan(cursor, tasks):
    done_tasks = [task[0] for task in tasks if task[1]]
    not_done_tasks = [task[0] for task in tasks if not task[1]]
    cursor.execute("""
        (
            SELECT user_id FROM user_tasks
            WHERE is_done = TRUE AND is_hidden = FALSE AND task_id IN (%s)
            GROUP BY user_id
            HAVING COUNT(*) = %s
        ) INTERSECT (
            SELECT user_id FROM user_tasks
            WHERE is_done = FALSE AND is_hidden = FALSE AND task_id IN (%s)
            GROUP BY user_id
            HAVING COUNT(*) = %s
        );
    """, [done_tasks, len(done_tasks), not_done_tasks, len(not_done_tasks)])

    res = [rec[0] for rec in cursor.fetchall()]
    return res

#return admin_id or GroupExistError
def get_admin(cursor, group_name):
    pass