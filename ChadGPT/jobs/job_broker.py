import os
import time
import re

import aiohttp
import asyncio

import os
import sys
sys.path.append(os.path.dirname(__file__))

from connectors.chatgpt_connector import ChatGPTConnector

class JobBroker: 
    def __init__(self):
        pass

    def run_jobs(self, job_params):
        async def _run_jobs():
            results = await asyncio.gather(*(self.run_job(job_param) for job_param in job_params))
            return results
        return asyncio.run(_run_jobs())

    async def run_job(self, job_param):
        async with aiohttp.ClientSession() as session:
            
            if job_param['llm'] == 'ChatGPT':
                connector = ChatGPTConnector()

            if job_param['operation'] == 'Get Answer':
                query = job_param['query']
                message = [ 
                    {"role": "system", "content": "You are an intellgent agent."},
                    {"role": "user", "content": query, }
                ]
                reply = await connector.send(message, session)
            elif job_param['operation'] == 'Get Agreement':
                float_pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
                reply = 'not a float'
                while not re.match(float_pattern, str(reply)):
                    query = f'How much semantic agreement are this two statements, from a scale of 0 to 1? \n {job_param["query"][0]} \n {job_param["query"][1]} \n ONLY RETURN A FLOAT IN YOUR RESPONSE, YOU CANNOT USE WORDS.'
                    message = [ 
                        {"role": "system", "content": "You are a semantic similarity scoring agent that provides a float between 0 to 1 representing semantic agreement. ONLY RETURN A FLOAT IN YOUR RESPONSE, YOU CANNOT USE WORDS."},
                        {"role": "user", "content": query, }
                    ]
                    reply = await connector.send(message, session)
                    reply = float(reply)
            else:
                raise ValueError('Operation not supported')
        
            
             
        return reply