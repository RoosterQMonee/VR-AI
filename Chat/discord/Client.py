import os
import json
import requests
import discord
import server
import threading

API_URL = 'https://api-inference.huggingface.co/models/TheDiamondKing/'

class MyClient(discord.Client):
    def __init__(self, model_name):
        super().__init__()
        self.api_endpoint = API_URL + model_name
        huggingface_token = os.environ['HUGGINGFACE_TOKEN']
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(huggingface_token)
        }

    def query(self, payload):
        data = json.dumps(payload)
        response = requests.request('POST',
                                    self.api_endpoint,
                                    headers=self.request_headers,
                                    data=data)
        ret = json.loads(response.content.decode('utf-8'))
        return ret

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.query({'inputs': {'text': 'Hello!'}})

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        #if message.channel.id == 940027282188300360:

        payload = {'inputs': {'text': message.content}}

        async with message.channel.typing():
          response = self.query(payload)
        bot_response = response.get('generated_text', None)
        
        if not bot_response:
            if 'error' in response:
                bot_response = '`Error: {}`'.format(response['error'])
            else:
                bot_response = 'Hmm... something is not right.'

        await message.reply(bot_response)

def main():
    client = MyClient('DialoGPT-small-harrypotter')
    client.run(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
  server.keep_alive()
  main()
