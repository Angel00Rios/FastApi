"""
Smart store API.

#----------------------------------------------------------------------------------------
# Description      : REST API.
#                    Modules and code for Python Python 3.9
#
# Requirements.    : fastapi
#                    uvicorn
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
from fastapi import FastAPI, status, Security, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader

# functionality
import functionality
import ia

# Get the full path where this program exist.
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
# Get the project directory.
PROJECT_DIR = os.path.dirname(WORKING_DIR)
# Logging configuration.
LOG = logging.getLogger()

API_KEY_H = APIKeyHeader(name='AccessKey', auto_error=False)

# FastAPI app
APP = FastAPI(title="Smart store",
              description="API to handle data.",
              version="0.9.0",
              docs_url="/")

#---------- AUTHENTICATION METHOD ---------------------------------------------------------------------------

async def check_auth(token: str = Security(API_KEY_H)):
    """Check access token."""
    if str(token) not in os.environ['ACCESSKEY']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

#---------- API METHODS ---------------------------------------------------------------------------
@APP.get("/productos_viables")
async def get_productos(_=Depends(check_auth)):
    """Obtener historial de ventas de un product"""
    conn = functionality.connection(os.environ["DBHOSTNAME"], os.environ["DBUID"],
                                    os.environ["DBPWD"], os.environ["DBNAME"], os.environ["PORT"])
    return functionality.get_productos(conn)

@APP.get("/prediccion_de_ventas")
async def get_ai(product_id: str, _=Depends(check_auth)):
    """POST information."""
    conn = functionality.connection(os.environ["DBHOSTNAME"], os.environ["DBUID"],
                                    os.environ["DBPWD"], os.environ["DBNAME"], os.environ["PORT"])
    data = functionality.get_product_hitoric(conn, str(product_id))
    return ia.get_ai(data)

@APP.get("/health")
async def healthcheck(_=Depends(check_auth)):
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
data = {'ID': '',
        'Existencia': '155',
        'Necesario': '120'}