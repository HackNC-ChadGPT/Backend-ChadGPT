import os
import time
import re

import aiohttp
import asyncio

import os
import sys
sys.path.append(os.path.dirname(__file__))

from connectors.chatgpt_connector import ChatGPTConnector

import yaml
with open('config.yml', 'r') as f: #TODO: global ConfigLoader class maybe?
    config = yaml.safe_load(f)

class JobBroker: 
    def __init__(self):
        self.semaphore = asyncio.Semaphore(config['broker']['max_concurrent_jobs'])

    def exponential_backoff_time(tries):
        min(config['broker']['base'] ** tries, config['broker']['max_wait'])

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
                reply = None
                tries = 0
                while reply is None and tries < config['broker']['max_retries']:
                    query = job_param['query']
                    message = [ 
                        {"role": "system", "content": "You are an intellgent agent."},
                        {"role": "user", "content": query, }
                    ]
                    reply = await connector.send(message, session)
                    tries += 1
                    time.sleep(self.exponential_backoff(tries))

            elif job_param['operation'] == 'Get Agreement':
                float_pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
                reply = 'not a float'
                tries = 0
                while not re.match(float_pattern, str(reply)) and tries < config['broker']['max_retries']:
                    query = f'How much semantic agreement are this two statements, from a scale of 0 to 1? \n {job_param["query"][0]} \n {job_param["query"][1]} \n ONLY RETURN A FLOAT IN YOUR RESPONSE, YOU CANNOT USE WORDS.'
                    message = [ 
                        {"role": "system", "content": "You are a semantic similarity scoring agent that provides a float between 0 to 1 representing semantic agreement. ONLY RETURN A FLOAT IN YOUR RESPONSE, YOU CANNOT USE WORDS."},
                        {"role": "user", "content": query, }
                    ]
                    reply = await connector.send(message, session)
                    reply = float(reply) if reply is not None else reply
                    tries += 1
                    time.sleep(self.exponential_backoff_time(tries))
            else:
                raise ValueError('Operation not supported')
        
            if reply is None or reply == 'not a float':
                raise ValueError(f'Job failed, too many tries: {message}')
             
        return reply
