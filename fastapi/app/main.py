from typing import Union
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from typing import Union
from typing_extensions import Annotated
from pydantic import BaseModel
import tarantool
import mmh3
import uuid
import logging

app = FastAPI()

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

connection = tarantool.Connection('localhost', 3302)


class Dialog(BaseModel):
    from_user: str
    to_user: str
    text: str


@app.post("/api/v1/dialog/send")
async def create_item(dialog: Dialog, x_tracing_id: Annotated[Union[str, None], Header()] = None):
    
    LOGGER.info('Receive request /api/v1/dialog/send (trace-id: %s)  params = %s', x_tracing_id, dialog.dict())

    dialog_id = send_dialog(dialog.from_user, dialog.to_user, dialog.text)

    content = {"dialog_id": dialog_id}

    if x_tracing_id is None:
        x_tracing_id = str(uuid.uuid4())
    headers = {"X-Tracing-Id": x_tracing_id}

    if dialog_id is None:
        return JSONResponse(status_code=500, content=content, headers=headers)
    else:    
        return JSONResponse(status_code=201, content=content, headers=headers)


#get dialog list
@app.get("/api/v1/dialog/list")
def list_dialog(from_user, to_user, x_tracing_id: Annotated[Union[str, None], Header()] = None):

    LOGGER.info('Receive request /api/v1/dialog. (trace-id: %s) from_user = %s to_user = %s', x_tracing_id, from_user, to_user)

    if x_tracing_id is None:
        x_tracing_id = str(uuid.uuid4())
    headers = {"X-Tracing-Id": x_tracing_id}

    dialogs = list_dialog(from_user, to_user)
    if dialogs is None:
        return JSONResponse(status_code=404, headers=headers)
    else:

        content = []

        for element in dialogs[0]:

            content.append({"from_user": str(element[2]), "to_user": str(element[3]), "text": element[4]})

        print(content)

        return JSONResponse(content=content, headers=headers)



def get_dialog_id(user1, user2):
    user1_hash = mmh3.hash(user1, signed=False)
    user2_hash = mmh3.hash(user2, signed=False)

    if user1_hash < user2_hash:
        dialog_id = user1 + user2
    else:
        dialog_id = user2 + user1

    return dialog_id


#SEND DIALOG
def send_dialog(from_user_id, to_user_id, text):

    dialog_id = get_dialog_id(from_user_id, to_user_id)

    try:
        response = connection.call('new_dialog', (dialog_id, from_user_id, to_user_id, text))
        new_dialog_uuid = response.data[0]
    except connection.Error as err:
        
        LOGGER.warning('Error saving dialog: %s', err)
        return None

    return new_dialog_uuid

#GET LIST of DIALOGS
def list_dialog(from_user_id, to_user_id):

    dialog_id = get_dialog_id(from_user_id, to_user_id)

    try:
        response = connection.call('get_dialog', (dialog_id))
        dialogs = response.data
    except connection.Error as err:
        
        LOGGER.warning('Error saving dialog: %s', err)
        return None

    return dialogs    

