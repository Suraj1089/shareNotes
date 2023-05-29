from os import environ
from Bard import Chatbot
from fastapi import APIRouter,Request
import pandas as pd 

router = APIRouter(
    tags=['Recommendation']
)


BARD_TOKEN = environ.get("BARD_TOKEN")

chatbot = Chatbot(BARD_TOKEN)

data = chatbot.ask("python project for beginner")

print(data['content'])
print(data.keys())
