import asyncio
from ollama import AsyncClient
import re

class ai():
    def __init__(self):
        pass

    async def chat(self, text):
        message = {'role': 'user', 'content': text}
        response = await AsyncClient().chat(model='deepseek-r1:14b', messages=[message])

        return re.sub(r'<think>.*?</think>', '', response['message']['content'], flags=re.DOTALL)




if __name__ == "__main__":
    inteleg = ai()
    print(asyncio.run(inteleg.chat('what is the best language for esp32?')))
