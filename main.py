import os
import streamlit as st
import time
from pineconeService import PineconeService
from assistantService import AssistantService
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
PINECONE_API_KEY = config['DEFAULT']['PINECONE_API_KEY']
PINECONE_ENV = config['DEFAULT']['PINECONE_ENV']
os.environ['OPENAI_API_KEY'] = config['DEFAULT']['OPENAI_API_KEY']

pinecone_service = PineconeService(PINECONE_API_KEY, PINECONE_ENV)
assistant_service = AssistantService(pinecone_service)

separator = '-_-'


if 'messages' not in st.session_state:
    st.session_state['messages'] = ''

if 'index' not in st.session_state:
    st.session_state['index'] = 0


st.title("Conversational bot")

conversation = st.session_state['messages'].split(separator)

for message in conversation:
    st.write(message)
text = st.empty()
message = text.text_input("Escribe tu mensaje", key='message{}'.format(st.session_state['index']), value='')

if message:
    response = assistant_service.send_message(st.session_state['messages'],  message)
    st.session_state['messages'] = st.session_state['messages'] + message + separator + response + separator
    
    #seguir explorando por este lado, tiene que ser por aca
    st.session_state.__delitem__('message{}'.format(st.session_state['index']))
    st.session_state['index'] += 1
    st.experimental_rerun()



    