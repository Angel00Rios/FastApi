"""
Offerings ODS API.

#----------------------------------------------------------------------------------------
# Description      : REST API, process files and save it to local directory.
#                    Modules and code for Python Python 3.7.3.
#
# Requirements.    : fastapi
#                    uvicorn
#
# Creation Date    : 2020-07-20
# Author           : [AR] angel.rios@ibm.com
#
# Revision history : 2020-07-20 - [AR] Initial version.
#----------------------------------------------------------------------------------------
"""
# Log handling.
import logging

# System and OS related functionality.
import os

# Data wrangling
#import pandas as pd

# Enconder JSON
from fastapi.encoders import jsonable_encoder

# Fast api functionality
from fastapi import FastAPI, status#, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
#from fastapi.security.api_key import APIKeyHeader

# functionality
import functionality

# Get the full path where this program exist.
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
# Get the project directory.
PROJECT_DIR = os.path.dirname(WORKING_DIR)
# Logging configuration.
LOG = logging.getLogger()

# FastAPI app
APP = FastAPI(title="Smart store",
              description="API to handle data.",
              version="0.9.0",)

#---------- API METHODS ---------------------------------------------------------------------------

@APP.get("/get")
async def get(table: str, key: str = None, valuekey: str = None,
                   columns: str = None):
    """Get information."""
    if columns:
        columns = ", ".join(columns)
    else:
        columns = '*'
    conn = functionality.connection(os.environ["dbhostname"], os.environ["dbuid"],
                                    os.environ["dbpwd"], os.environ["dbname"])
    if key:
        result = functionality.select_by_key(conn, table, key, valuekey, columns)
    else:
        result = functionality.select(conn, table, columns)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'status': result})

@APP.post("/post")
async def post(data: dict, table: str):
    """POST information."""
    data = jsonable_encoder(data)
    LOG.info(data)
    conn = functionality.connection(os.environ["dbhostname"], os.environ["dbuid"],
                                    os.environ["dbpwd"], os.environ["dbname"])
    functionality.insert(conn, data, table)
    return JSONResponse(status_code=status.HTTP_200_OK)

@APP.put("/put")
async def put(data: dict, table: str, key: str):
    """POST information."""
    data = jsonable_encoder(data)
    LOG.info(data)
    conn = functionality.connection(os.environ["dbhostname"], os.environ["dbuid"],
                                    os.environ["dbpwd"], os.environ["dbname"])
    functionality.update(conn, data, table, key)
    return JSONResponse(status_code=status.HTTP_200_OK)

@APP.get("/health")
async def healthcheck():
    """Health check used to monitor from New Relic."""
    return JSONResponse(status_code=status.HTTP_200_OK, content={'status': 'alive'})

#---------- GENERAL METHODS -----------------------------------------------------------------------

def init_logger(level: str) -> None:
    """
    Initialize logger configuration.

    :params level: Log level (CRITICAL || ERROR || WARNING || INFO || DEBUG).
    """
    # Set logging level
    LOG.setLevel(level)

    # Stream handler for human consumption and stderr.
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter("%(asctime)s - "
                                         "%(levelname)s - "
                                         "%(message)s")

    stream_handler.setFormatter(stream_formatter)
    LOG.addHandler(stream_handler)
    LOG.propagate = False

# Set log level.
init_logger(os.environ["LOGLEVEL"])
# Get environment config.
CONF = functionality.read_file(os.path.join(PROJECT_DIR, "conf", "api.conf"), "json")
