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

    #Create groups
    groups = [
        ("Algebra", "Jdan."), 
        ("BD-lectures", "Roslovcev, philosophy class."), 
        ("BD-practice", "The best.")
    ]

    for i in range(len(groups)):
        BD.create_group(cursor, users[i], groups[i][0], groups[i][1])

    #Create user_groups
    for user in users:
        for j in range(len(groups)):
            group = groups[j]
            admin = users[j]
            if admin == user:
                continue

            BD.join_user(cursor, user, group[0], admin)

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


    #Create tasks
    tasks = []
    for project in projects:
        for i in range(random.randint(0, 4)):
            task_info = "Task #" + str(i) + " of " + project[1]
            tasks.append((project[0], task_info, project[1]))
            BD.create_task(cursor, *tasks[~0])

    #Create user_tasks
    for task in tasks:
        for user in users:
            BD.set_task(cursor, user, task[1], bool(random.randint(0, 1)), bool(random.randint(0, 1)))

    conn.commit()

if __name__ == "__main__":
    main()
