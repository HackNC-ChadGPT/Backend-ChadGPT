import openai
import os
import asyncio

import yaml
with open('config.yml', 'r') as f: #TODO: global ConfigLoader class maybe?
    config = yaml.safe_load(f)

class ChatGPTConnector():
    def __init__(self):
        openai.api_key = os.environ.get(config['connector']['chatgpt']['api_key_var_name'])
        self.model = config['connector']['chatgpt']['model']
        
    async def send(self, messages, session):
        openai.aiosession.set(session)
        chat = await openai.ChatCompletion.acreate( 
            model = self.model, 
            messages=messages 
        )
        reply = chat.choices[0].message.content
        # openai.aiosession.get().close()
        return reply

