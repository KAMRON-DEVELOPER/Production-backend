from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer


class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print('Websocket Connecting...', event)
        self.send({
            'type': 'websocket.accept'
        })
        
    def websocket_receive(self, event):
        print('Websocket Receved...', event['text'])
        
    def websocket_disconnect(self, event):
        print('Websocket Disconnecting...', event)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print('Websocket Connected...', event)
        await self.send({
            'type': 'websocket.accept'
        })
        
    async def websocket_receive(self, event):
        print('Websocket Receved...', event['text'])
        await self.send({
            'type': 'websocket.send',
            'text': 'response from Kamronbek!'
        })
        
    async def websocket_disconnect(self, event):
        print('Websocket Disconnected...', event)
        raise StopConsumer()

