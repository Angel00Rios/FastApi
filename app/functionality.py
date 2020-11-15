"""
Process.

#----------------------------------------------------------------------------------------
# Creation Date    : 2020-11-14
# Author           : [AR] Angel Rios <angel00rios@yahoo.com>
#
# Revision history : 2020-11-14 - [AR] Initial version.
#----------------------------------------------------------------------------------------
"""
# System and OS related functionality.
import os

# Log Handling.
import logging

# Dara wrangling
import pandas as pd

# Json Handling
import json

# Sql
import pymysql.cursors

# Logging configuration will be __main__ as this code should run by itself.
LOG = logging.getLogger(__name__)

# Get the full path where this program exist.
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))

# Get the project directory.
PROJECT_DIR = os.path.dirname(WORKING_DIR)

def connection(host, user, password, db, charset = 'utf8'):
    try:
        connection = pymysql.connect(host = host,
                                     user = user,
                                     password = password,
                                     db = db,
                                     charset =  'utf8',
                                     cursorclass = pymysql.cursors.DictCursor)
    except pymysql.Error as e:
        raise EnvironmentError(e)
    return connection

def select_by_key(connection, tabla, key, key_value, columns = "*"):
    try:
        with connection.cursor() as cursor:
            # Read a single record
            #sql = "SELECT `userName`, `password` FROM `users`"
            sql = "Select {} from {} Where {} = '{}'".format(columns, tabla, key, key_value)
            logger.info(sql)
            cursor.execute(sql)
            result = cursor.fetchone()
            logger.info(result)
    except pymysql.Error as e:
        raise EnvironmentError(e)
    #finally:
    #    connection.close()
    return result

def select(connection, tabla, columns = "*"):
    try:
        with connection.cursor() as cursor:
            # Read a single record
            #sql = "SELECT `userName`, `password` FROM `users`"
            sql = "Select {} from {} ".format(columns, tabla)
            logger.info(sql)
            cursor.execute(sql)
            sql_values = cursor.fetchall()
            logger.info(sql_values)
    except pymysql.Error as e:
        raise EnvironmentError(e)
    #finally:
    #    connection.close()
    return sql_values

def insert(connection, dictio, table):
    before_to_insert([dictio])
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO {0} ({1}) VALUES ({2}) ".format(table, ", ".join(dictio.keys()).lower(),
                                                                ",".join(str(v.encode("utf-8")) for v in dictio.values()))
            logger.info(sql)
            cursor.execute(sql)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except pymysql.Error as e:
        raise EnvironmentError(e)
    #finally:
    #    connection.close()

def update(connection, dic, table, key):
    before_to_insert([dic])
    lista = []
    value = dic[key]
    # Create a update sql statement
    for column, row in dic.iteritems():
        lista.append(column.lower() + ' = ' + str(row.encode("utf-8")))
    sql = "UPDATE {0} SET {1} where {2} = {3}".format(table, ', '.join(lista), key, value)
    try:
        with connection.cursor() as cursor:
            # 
            cursor.execute(sql)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except pymysql.Error as e:
        raise EnvironmentError(e)
    #finally:
    #    connection.close()

def delete_by_key(connection, tabla, key):
    try:
        with connection.cursor() as cursor:
            # Read a single record
            #sql = "SELECT `userName`, `password` FROM `users`"
            sql = "DELETE from {} Where cellphone = {}".format(tabla, key)
            cursor.execute(sql)
            result = cursor.fetchone()
    except pymysql.Error as e:
        raise EnvironmentError(e)
    #finally:
    #    connection.close()
    return result

def before_to_insert(dictionaries_list):
    """Modify the values of a list of dictionaries for insert them into the database.\n
    Input:
    dictionaries_list    -> dictionaries to fill with the necesary information
                            for each insert in the DB
    List of keys of string columns to add single quotes.
    If is a void field convert this one to NULL
    """
    for dic in dictionaries_list:
        for key in dic:
            if dic[key] is None:
                dic[key] = 'NULL'
    #if is different of only with space and at least one character
            elif  dic[key].isspace() is True:
                dic.update({key:"NULL"})
            elif dic[key] and dic[key] != "NULL":
                dic.update({key: "'" + escape_apostrophe(dic[key]) + "'"})
            else:
                dic.update({key:"NULL"})

def escape_apostrophe(_string):
    '''
    This function will duplicate each apostrophe
    '''
    return "''".join(_string.split("'"))

def read_file(conf_file: str, format_: str) -> object:
    """
    Load .config file and returns a config dict.

    :param conf_file: Path to config file.
    :return: Mixed dict or plain text values.
    """
    try:
        with open(conf_file, 'r') as file:
            config = file.read()
        config = json.loads(config) if format_ == 'json' else config
    except:
        LOG.error("Could not open config file: %s", conf_file, exc_info=True)
        raise
    else:
        LOG.info('Configuration [%s] file loaded. %s', format_, conf_file)
        return config