import random
import psycopg2
import BD

def main():
    conn_string = "host='localhost' dbname='botannet' user='postgres' password='secret'"
    print("Connecting to database\n ->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("Connected!")

    # Create users
    users = list(range(10)) + [239017, 12345, 100]
    for user in users:
        BD.create_user(cursor, user)


    cursor.execute("TABLE users;")
    print(cursor.fetchall())

    # for user in users:
    #     BD.delete_user(cursor, user)


    # cursor.execute("TABLE users;")
    # print(cursor.fetchall())

    #Create groups
    groups = [
        ("Algebra", "Jdan."), 
        ("BD-lectures", "Roslovcev, philosophy class."), 
        ("BD-practice", "The best.")
    ]

    for i in range(len(groups)):
        BD.create_group(cursor, users[i], groups[i][0], groups[i][1])

    # for i in range(len(groups)):
    #     BD.delete_group(cursor, users[i], groups[i][0])

    #Create user_groups
    for user in users:
        for j in range(len(groups)):
            group = groups[j]
            admin = users[j]
            if admin == user:
                continue

            BD.join_user(cursor, user, group[0], admin)

    # cursor.execute("TABLE groups;")
    # print(cursor.fetchall())

    # cursor.execute("TABLE user_groups;")
    # print([rec for rec in cursor.fetchall() if rec[2]])

    # for j in range(len(groups)):
    #     group = groups[j]
    #     admin = users[j]
    #     print("DELETE ", admin, group[0])
    #     cursor.execute("TABLE groups;")
    #     print(cursor.fetchall())
    #     BD.unjoin_user(cursor, admin, group[0], admin)
            

    #Create projects
    projects = []
    for i in range(len(groups)):
        admin_id = users[i]
        group_name = groups[i][0]
        for j in range(3):
            project_name = "Project #" + str(j) + " of group " + group_name
            project_info = "useless info"
            projects.append((admin_id, project_name, group_name, project_info))

    for project in projects:
        BD.create_project(cursor, *project)

    # for project in projects:
    #     BD.delete_project(cursor, project[0], project[1])

    # cursor.execute("TABLE projects;")
    # print(cursor.fetchall())


    # Create tasks
    tasks = []
    for project in projects:
        for i in range(random.randint(0, 4)):
            task_info = "Task #" + str(i) + " of " + project[1]
            tasks.append((project[0], task_info, project[1]))
            BD.create_task(cursor, *tasks[~0])

    # cursor.execute("TABLE tasks;")
    # print(cursor.fetchall())

    # for task in tasks:
    #     BD.delete_task(cursor, task[0], task[1])

    # cursor.execute("TABLE tasks;")
    # print(cursor.fetchall())

    #Create user_tasks
    for task in tasks:
        for user in users:
            BD.set_task(cursor, user, task[1], bool(random.randint(0, 1)), bool(random.randint(0, 1)))

    # find_tasks = []
    # for i in range(2):
    #     task_id = BD.get_task_id(cursor, tasks[random.randrange(0, len(tasks))][1])
    #     find_tasks.append((task_id, bool(random.randint(1, 1))))

    # print(BD.find_botan(cursor, find_tasks))
    # cursor.execute("TABLE user_tasks")
    # records = cursor.fetchall()
    # done = dict()
    # not_done = dict()
    # for record in records:
    #     done[record[1]] = []
    #     not_done[record[1]] = []

    # for record in records:
    #     if record[2] and not record[3]:
    #         done[record[1]].append(record[0])
    #     if not record[2] and not record[3]:
    #         not_done[record[1]].append(record[0])

    # print("done:")
    # for task_id in done:
    #     print(str(task_id) + " done by " + str(done[task_id]))

    # print("not done:")
    # for task_id in not_done:
    #     print(str(task_id) + " not done by " + str(not_done[task_id]))


    # conn.commit()

if __name__ == "__main__":
    main()
