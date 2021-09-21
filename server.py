import logging

import socketio
import uvicorn
from uvicorn.loops.uvloop import uvloop_setup
from socketio.exceptions import ConnectionRefusedError

# Set some basic logging
logging.basicConfig(
    level=2,
    format="%(asctime)-15s %(levelname)-8s %(message)s"
)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*' )
app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ, auth):
    logging.info(f"connect {sid}")
    # raise ConnectionRefusedError('authentication failed')

@sio.event
async def disconnect(sid):
    logging.info(f'disconnect {sid}')

async def send_message_to_client():
    await sio.emit('my message to harshit', {
        'data': 'Hello world from server'
    })

async def background_task_1():
    while True:
        await sio.emit('my message to harshit', {
            'data': 'Hello world from server'
        })
        await sio.sleep(2)

@sio.event
async def send_changes(sid, data):
    # print("message ", data)
    await sio.emit('recieve_changes', data)

@sio.on("message_from_client")
async def message_from_client(sid, data):
    print(data)
    await sio.sleep(2)
    sio.start_background_task(background_task_1)

@sio.event
async def another_event(sid, data):
    print('sid: ', sid)
    print('data: ', data)
    return "Something just like this"

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
