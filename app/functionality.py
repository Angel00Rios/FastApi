"""
Process.

#----------------------------------------------------------------------------------------
# Author           : [AR] Angel Rios <angel00rios@yahoo.com>
#
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
            LOG.info(sql)
            cursor.execute(sql)
            result = cursor.fetchone()
            LOG.info(result)
    except pymysql.Error as e:
        raise EnvironmentError(e)
    finally:
        connection.close()
    return result

def select(connection, tabla, columns = "*"):
    try:
        with connection.cursor() as cursor:
            # Read a single record
            #sql = "SELECT `userName`, `password` FROM `users`"
            sql = "Select {} from {} ".format(columns, tabla)
            LOG.info(sql)
            cursor.execute(sql)
            sql_values = cursor.fetchall()
            LOG.info(sql_values)
    except pymysql.Error as e:
        raise EnvironmentError(e)
    finally:
        connection.close()
    return sql_values

def get_productos(connection):
    try:
        with connection.cursor() as cursor:
            sql = read_file(os.path.join(PROJECT_DIR, "sql", "step1.sql"), "sql")
            LOG.info(sql)
            cursor.execute(sql)
            sql_values = cursor.fetchall()
            LOG.info(sql_values)
    except pymysql.Error as e:
        raise EnvironmentError(e)
    finally:
        connection.close()
    return sql_values

def get_product_hitoric(connection, product_id):
    try:
        with connection.cursor() as cursor:
            sql = read_file(os.path.join(PROJECT_DIR, "sql", "step1.sql"), "sql").format(product_id)
            LOG.info(sql)
            cursor.execute(sql)
            sql_values = cursor.fetchall()
            LOG.info(sql_values)
    except pymysql.Error as e:
        raise EnvironmentError(e)
    finally:
        connection.close()
    return sql_values

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