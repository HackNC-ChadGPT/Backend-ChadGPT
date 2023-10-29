import sys # TODO: Do packages properly
sys.path.append('../jobs/')
sys.path.append('./')
sys.path.append('../')
sys.path.append('C:/Users/Jing Wen/stuff/Backend-ChadGPT/ChadGPT/') # TODO: remove
from jobs.job_broker import JobBroker

import os
import sys

import yaml
with open('config.yml', 'r') as f: #TODO: global ConfigLoader class maybe?
    config = yaml.safe_load(f)


class Controller:
    def __init__(self):
        self.broker = JobBroker()

    def run(self, query):
        raise NotImplementedError

    def get_answers(self, query, n):
        job_params = [
            {
                'llm': 'ChatGPT',
                'operation': 'Get Answer',
                'query': query
            } for _ in range(n)
        ]
        return self.broker.run_jobs(job_params)

    def get_agreement(self, answers):
        job_params = []
        for i in range(len(answers)):
            for j in range(i + 1, len(answers)):
                job_params += [
                    {
                        'llm': 'ChatGPT',
                        'operation': 'Get Agreement',
                        'query': (answers[i], answers[j])
                    }
                ]
        return self.broker.run_jobs(job_params)

''' Example usage (in Flask):
class MyController(Controller):
    def run(self, query):
        answers = self.get_answers(query, 3)
        agreements = self.get_agreement(answers)
        return sum(agreements)/len(agreements)

result = MyController().run('What is the meaning of life?')
print(result)
'''
