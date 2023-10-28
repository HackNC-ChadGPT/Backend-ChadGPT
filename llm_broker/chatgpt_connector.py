import yaml
import openai
import os

with open('config.yml', 'r') as f: #TODO: global ConfigLoader class maybe?
    config = yaml.safe_load(f)

class ChatGPTConnector():
    def __init__(self):
        openai.api_key = os.environ.get(config['connector']['chatgpt']['api_key_var_name'])
        self.model = config['connector']['chatgpt']['model']

    def send(self, messages):
        chat = openai.ChatCompletion.create( 
            model = self.model, 
            messages=messages 
        )
        reply = chat.choices[0].message.content

        return reply

