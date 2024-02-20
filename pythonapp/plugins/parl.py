from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from langchain.memory import CassandraChatMessageHistory, ConversationBufferMemory
from langchain_openai import OpenAI
#from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
#from langchain_community.llms import BaseLLM
import json
from gtts import gTTS
import tempfile
import os
import speech_recognition as sr
import pygame
from pydub import AudioSegment
from pydub.playback import play
import time
import librosa
import numpy as np
import simpleaudio as sa
import threading

cloud_config= {
  'secure_connect_bundle': 'secure-connect-npc-one.zip'
}



ASTRA_DB_KEYSPACE = "default_keyspace"
OPENAI_API_KEY = ""

cluster = Cluster(cloud=cloud_config, auth_provider=PlainTextAuthProvider("token", "AstraCS:SEMFaXnCrvbjwXkrwBRYRikt:7566ef20077b813d50858b9c70a3e5cfc2aadf4379e8fa04c8516cbc15d897d3"))
session = cluster.connect()

message_history = CassandraChatMessageHistory(
    session_id="anything",
    session=session,
    keyspace=ASTRA_DB_KEYSPACE,
    ttl_seconds=3600
)

message_history.clear()

cass_buff_memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=message_history
)

global memory_key

chat_his = ""
human_input = "start"

template = """
you are to simulate an AI of a user driven Adventure in 20 words that depends on the human_input to continue

A traveler named Elara seeks the lost Gem of Serenity. 
You must navigate her through challenges, choices, and consequences, 
dynamically adapting the tale based on the traveler's decisions. 
Your goal is to create a branching narrative experience where each choice 
leads to a new path or could lead to death, ultimately determining Elara's fate.
make dumb suggestions kill elara
dont ask to clarify if its a dumb choice

Here are some rules to follow:
1. Start by asking the player to choose some kind of weapons that will be used later in the game


Here is the chat history, use this to understand what to say next: {chat_history}

Human: {human_input}
AI:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"],
    template=template
)

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=cass_buff_memory
)

choice = "start"

while True:
    response = llm_chain.predict(human_input=choice)
    print(response.strip())

    if "The End." in response:
        break

    choice = input("Your reply: ")