import os
import sys
sys.path.append(os.path.dirname(__file__))
from connectors.connector import Connector

import openai
import asyncio

import yaml
with open('config.yml', 'r') as f: #TODO: global ConfigLoader class maybe?
    config = yaml.safe_load(f)

class ChatGPTConnector(Connector):
    ''' A connector that uses OpenAI's ChatGPT API. Implements
    two methods compulsory for the Connector interface: the
    constructor and a send method that awaits a string response
    from ChatGPT to a prompt.
    '''
    def __init__(self):
        openai.api_key = os.environ.get(
            config['connector']['chatgpt']['api_key_var_name'])
        self.model = config['connector']['chatgpt']['model']
        
    async def send(self, messages, session):
        openai.aiosession.set(session)
        chat = await openai.ChatCompletion.acreate( 
            model = self.model, 
            messages=messages 
        )
        reply = chat.choices[0].message.content
        return reply

