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

# Logging configuration will be __main__ as this code should run by itself.
LOG = logging.getLogger(__name__)

# Get the full path where this program exist.
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))

# Get the project directory.
PROJECT_DIR = os.path.dirname(WORKING_DIR)

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