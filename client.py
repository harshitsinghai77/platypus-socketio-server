import asyncio
import socketio
import uvloop

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print("connection established")

@sio.event
def connect_error(data):
    print('data: ', data)
    print("The connection failed!")

@sio.event
async def disconnect():
    print('disconnected from server')

def recieved_call_back(data):
    print(data)

async def my_message():
    # await sio.emit('my custom event', {'response': 'my response'}, callback=recieved_call_back)
    await sio.emit('message_from_client', {'hello': 'world'})
    
@sio.on('my message to harshit')
async def on_message_change(data):
    print(data)
    # await sio.emit('message_from_client', {'hello': 'world'})

async def send_message_to_server():
    await sio.emit('message_from_client', {'data': 'Hello world from client'})

async def main():
    await sio.connect('http://127.0.0.1:5000')
    await my_message()
    await sio.wait()
    
if __name__ == '__main__':
    uvloop.install()
    asyncio.run(main())