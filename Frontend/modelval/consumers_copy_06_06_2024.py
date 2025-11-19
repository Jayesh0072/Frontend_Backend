import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from . import models
from modelval.models import Thread, Chatmessage
import traceback
from urllib.parse import parse_qs
# from modelvalidation.rmseviews import thread_filter_creation

User = get_user_model()

# websocket connection
class ChatConsumer(AsyncConsumer):
    # async def websocket_connect(self, event):
    #     print('connected', event)
    #     # print("request",request.session['uid'])
    #     user = self.scope['user']
    #     # user = models.Users.objects.get(u_aid = 12)
    #     chat_room = f'user_chatroom_{user.id}'
    #     self.chat_room = chat_room
    #     await self.channel_layer.group_add(
    #         chat_room,
    #         self.channel_name
    #     )
    #     await self.send({
    #         'type': 'websocket.accept'
    #     })
    async def websocket_connect(self, event): 
        try:
            dict = {}
            print("check------------1",self.scope["query_string"])
            # a = str(self.scope["query_string"])
            # b = a.split('=')
            # print("b",b)
            # c = b[1].split('&')
            # dict['id'] = c[0]
            # dict['type'] = b[2]
            # print("dict new",dict)
            
            # print("request",request.session['uid'])
            # user = await self.get_user_object(int(self.scope["query_string"]))
            # chat_room = 'user_chatroom_M0701000'
            # if dict['type'] == "model'":
            #     chat_room = 'user_chatroom_'+dict['id']
            # else:
            #     chat_room = 0
            query_string = parse_qs(self.scope['query_string'])
            if b'type' in query_string:
                if query_string[b'type'][0] ==b'model':
                    chat_room = 'user_chatroom_'+str(query_string[b'room'][0].decode())
                else:
                    user = await self.get_user_object(int(str(query_string[b'room'][0].decode())))
                    chat_room='user_chatroom_'+str(user.u_aid)
             
            self.chat_room = chat_room
            print('chat_room ',chat_room, ' connected')
            await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )
            await self.send({
                'type': 'websocket.accept'
            })
        except Exception as e:
            print(e,', ',traceback.print_exc())
    #any message received
    async def websocket_receive(self, event):
        try:
            print('receive once', event)
            received_data = json.loads(event['text'])
            msg = received_data.get('message')
            sent_by_id = received_data.get('sent_by')
            # print("sent_by_id-1",sent_by_id)
            send_to_id = received_data.get('send_to')
            type = received_data.get('type') 
            mdl_id = received_data.get('mdl_id')
            commented_by = received_data.get('commented_by')  
            # print("send_to_id-2",send_to_id)
            # send_to_id = 3
            # user1 = models.Users.objects.get(u_aid = sent_by_id)
            # user2 = models.Users.objects.get(u_aid = send_to_id)
            # thread_obj = models.Thread.objects.get(first_person = user1,second_person = user2)
            # print("thread_obj",thread_obj)
            
            thread_id = received_data.get('thread_id')
            response = {
                'message': msg,
                'sent_by': sent_by_id,#self_user.id,
                'thread_id': thread_id,
                'type':type,
                'mdl_id':mdl_id,
                'commented_by':commented_by
            }

            if type=='msg':
                await self.channel_layer.group_send(
                    'user_chatroom_'+mdl_id,
                    {
                        'type': 'chat_message',
                        'text': json.dumps(response)
                    }
                )
            else:
            # thread_ida = await self.get_thread_id(sent_by_id,send_to_id)
            # print("thread_id",thread_ida)

                if not msg:
                    print('Error:: empty message')
                    return False

                sent_by_user = await self.get_user_object(sent_by_id)
                # print("sent_by_user",sent_by_user.u_aid)
                send_to_user = await self.get_user_object(send_to_id)
                # print("send_to_user",send_to_user)
                thread_obj = await self.get_thread(thread_id)
                if not sent_by_user:
                    print('Error:: sent by user is incorrect')
                if not send_to_user:
                    print('Error:: send to user is incorrect')
                if not thread_obj:
                    print('Error:: Thread id is incorrect')

                await self.create_chat_message(thread_obj, sent_by_user, msg)

                other_user_chat_room = f'user_chatroom_{send_to_id}'
                self_user = sent_by_user.u_aid #self.scope['user']
                # print("other_user_chat_room",other_user_chat_room,'self.chat_room, ',self.chat_room)
                # print("self_user",self_user)
                # print("sent_by_id.u_aid",sent_by_id.u_aid)
            

                await self.channel_layer.group_send(
                    other_user_chat_room,
                    {
                        'type': 'chat_message',
                        'text': json.dumps(response)
                    }
                )

                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        'type': 'chat_message',
                        'text': json.dumps(response)
                    }
                )
        except Exception as e:
            print('error is ',e)
            print('stacktrace is ',traceback.print_exc())

    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user_object(self, user_id):
        print("user_id",user_id)
        qs = models.Users.objects.filter(u_aid=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(thread_id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        Chatmessage.objects.create(thread=thread, chat_user=user, message=msg)
 
    @database_sync_to_async
    def get_thread_id(self,send_by,send_to):
        threadfilter = Thread.objects.get(first_person = send_by,second_person = send_to)
        print("threadfilter",threadfilter)
        thread_id = threadfilter.id
        print("pass",thread_id)
        return thread_id

