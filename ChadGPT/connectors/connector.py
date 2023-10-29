import openai
import os
import asyncio

import yaml
with open('config.yml', 'r') as f: #TODO: global ConfigLoader class maybe?
    config = yaml.safe_load(f)

class Connector():
    def __init__(self):
        raise NotImplementedError()
        
    async def send(self, messages, session):
        raise NotImplementedError()

