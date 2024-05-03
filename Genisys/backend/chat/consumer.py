from channels.generic.websocket import AsyncJsonWebsocketConsumer


'''
--------------------------------------------------
            Chat canceled for no reason
--------------------------------------------------
'''
class chatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_name = None
        await self.accept()
    
    async def receive_json(self, content, **kwargs):
        event = content.get('event', None)
        group_id = content.get('id', None)
        if event == 'join_group':
            if self.group_name:
                await self.channel_layer.group_discard(self.group_name, self.channel_name)
            self.group_name = str(group_id)
            print("user joined")
            await self.channel_layer.group_add(self.group_name, self.channel_name)
        elif event == 'message':
            await self.channel_layer.group_send(self.group_name, {
                "type": "send_message",
                "data": content['message']
            })
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    


    async def send_message(self, event):
        await self.send_json(event['data'])