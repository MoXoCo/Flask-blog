import sqlite3
import sys

def table_select(old_conn):
    table_select = '''
    SELECT
        *
    FROM
        `sqlite_master`
    WHERE
        `type` = 'table'
    '''
    cursor = old_conn.execute(table_select)
    return cursor


def data_select(old_conn, tablename):
    sql_select = '''
    SELECT
        *
    FROM
        {}
    '''
    cursor = old_conn.execute(sql_select.format(tablename))
    return cursor


def data_insert(new_conn, cursor, tablename):
    sql_insert = '''
    INSERT INTO
        {}
    VALUES
        {}
    '''
    for data in cursor:
        #print('debug insert_data: ', data)
        new_conn.execute(sql_insert.format(tablename, data))


def create_db(old_conn, new_conn, cursor):
    values = cursor.fetchall()
    for table in values:
        #print('debug table: ', table)
        tablename = table[1]
        sql_create_table = table[-1]

        new_conn.execute(sql_create_table)
        data_cursor = data_select(old_conn, tablename)
        data_insert(new_conn, data_cursor, tablename)


def db_changes(old, new):
    old.commit()
    old.close()
    new.commit()
    new.close()


def main(old_db, new_db):
    old_conn = sqlite3.connect(old_db)
    new_conn = sqlite3.connect(new_db)
    cursor = table_select(old_conn)
    create_db(old_conn, new_conn, cursor)
    db_changes(old_conn, new_conn)


if __name__ == '__main__':
    old_db = sys.argv[1]
    new_db = sys.argv[2]
    main(old_db, new_db)
    print('数据库迁移成功！')