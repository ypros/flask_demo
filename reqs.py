import logging
import requests
from requests.exceptions import HTTPError

FASTAPI_URL = "http://localhost:8001"
SEND_DIALOG_METHOD = "/api/v1/dialog/send"
LIST_DIALOG_METHOD = "/api/v1/dialog/list"

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

#SEND DIALOG
def send_dialog(from_user_id, to_user_id, text):
    
    x_tracing_id = str(uuid.uuid4())
    headers = {"X-Tracing-Id": x_tracing_id}

    data = {"from_user": from_user_id, "to_user": to_user_id, "text": text}

    try:
        response = requests.post(FASTAPI_URL + SEND_DIALOG_METHOD, headers=headers, data=data)
        response.raise_for_status()
    except HTTPError as http_err:
        LOGGER.warning('send_dialog (traceid: %s): HTTP error occurred: %s', x_tracing_id, http_err)
    except Exception as err:
        LOGGER.error('send_dialog (traceid: %s): Other error occurred: %s)', x_tracing_id, err)
    else:
        LOGGER.info('send_dialog (traceid: %s): Success')

    return response.text

#LIST of DIALOGS
def list_dialog(from_user_id, to_user_id):
    
    x_tracing_id = str(uuid.uuid4())
    headers = {"X-Tracing-Id": x_tracing_id}

    params = {"from_user": from_user_id, "to_user": to_user_id}

    try:
        response = requests.post(FASTAPI_URL + SEND_DIALOG_METHOD, headers=headers, params=params)
        response.raise_for_status()
    except HTTPError as http_err:
        LOGGER.warning('list_dialog (traceid: %s): HTTP error occurred: %s', x_tracing_id, http_err)
    except Exception as err:
        LOGGER.error('list_dialog (traceid: %s): Other error occurred: %s)', x_tracing_id, err)
    else:
        LOGGER.info('list_dialog (traceid: %s): Success')

    return response.text