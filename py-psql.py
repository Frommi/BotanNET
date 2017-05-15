import psycopg2
import BD_functions

def init(cursor):
    cursor.execute(open("BotanNET_create_bd.sql", "r").read())

def main():
    conn_string = "host='localhost' dbname='botannet' user='postgres' password='secret'"
    print("Connecting to database\n ->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("Connected!")
    # init(cursor)
    BD_functions.delete_user(cursor, 239017)
    conn.commit()


if __name__ == "__main__":
    main()
