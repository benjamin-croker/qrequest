import json
import os
import re
import io
import csv

# set path names and db connection settings
SQL_PATH = "sql"
SETTINGS_FILENAME = os.path.join("settings", "settings.json")
with open(SETTINGS_FILENAME) as settings_fp:
    SETTINGS = json.load(settings_fp)


def construct_dict(cursor):
    """ transforms the db cursor rows from table format to a
        list of dictionary objects
    """
    rows = cursor.fetchall()
    return [dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in rows]


def construct_list(cursor):
    """ transforms the db cursor into a list of records,
        where the first item is the header
    """
    header = [h[0] for h in cursor.description]
    data = cursor.fetchall()
    return header, data


def construct_csv(cursor):
    """ transforms the db cursor rows into a csv file string
    """
    # def encode_row(row, encoding='utf-8'):
    #     return [r.encode(encoding) for r in row]
    header, data = construct_list(cursor)
    output = io.BytesIO()
    writer = csv.writer(output)

    writer.writerow(header)
    for row in data:
        writer.writerow(row)

    return output.getvalue()


def load_query(query_filename):
    with open(os.path.join(SQL_PATH, query_filename+'.sql')) as f:
        return f.read()


def get_params(query_filename):
    # returns a list of all the parameters in the sql file
    query_text = load_query(query_filename)
    return re.compile(r':(\w+)').findall(query_text)


def get_queries():
    # returns a list of all the sql files
    filenames = os.listdir(SQL_PATH)
    # filter for files ending in ".sql"
    return [f[:-4] for f in filenames if f[-4:] == ".sql"]


def get_driver(driver_name):
    if driver_name == 'sqlite3':
        import sqlite3 as db_driver
    elif driver_name == 'cx_Oracle':
        import cx_Oracle as db_driver
    elif driver_name == 'pyodbc':
        import pyodbc as db_driver
    elif driver_name == 'psycopg2':
        import psycopg2 as db_driver
    elif driver_name == 'PyMySql':
        import PyMySql as db_driver
    else:
        # TODO: pick a better exception type and message
        raise ImportError
    return db_driver


def run_query(query_filename, params_dict, data_format='list'):
    # set up a db connection from the settings
    db_driver = get_driver(SETTINGS['db_driver'])
    conn = db_driver.connect(SETTINGS['db_connection_string'])
    cursor = conn.cursor()

    # run the query
    cursor.execute(load_query(query_filename), params_dict)
    if data_format == 'list':
        # format into a table with header
        query_results = construct_list(cursor)
    elif data_format == 'dict':
        # format into dictionary
        query_results = construct_dict(cursor)
    elif data_format == 'csv':
        # format into dictionary
        query_results = construct_csv(cursor)
    conn.close()

    return query_results

