from groq import Groq
import os
import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection
import time
from pyairtable import Table

# create a title for the app

st.title("Startup Storyteller")

# create a description for the app

st.write("This app will generate personalized storytelling on your painpoint and will create an elevator pitch for your value proposition. For more information, please contact Dries Faems, https://www.linkedin.com/in/dries-faems-0371569/")



groq_api_key = st.text_input("Please provide your Groq API key. If you do not have a Groq API key, please got to https://console.groq.com/playground", type="password")

painpoint = st.text_input('Enter the painpoint that your startup is trying to solve')
persona = st.text_input('Describe the persona that is experiencing the painpoint')
valueproposition = st.text_input('Describe the value proposition of your startup')

# create click button to start

if st.button('Submit'):
    os.environ["GROQ_API_KEY"] = groq_api_key
    client = Groq()
    
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in painpoint storytelling. When developing the story, make it as personal as possible, considering the persona. The core of the storytelling is to trigger emotions and make sure that the audience is captivated by the story."
            },
            {
                "role": "user",
                "content": "Painpoint = " + painpoint + "; Persona = " + persona
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    text = ""
    for chunk in completion:
        text = text + str(chunk.choices[0].delta.content)
    st.markdown('**Personal storytelling on painpoint =**')
    st.write(text)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "Create a script for a two minute elevator pitch for a startup. I will provide you the painpoint, persona and value proposition."
            },
            {
                "role": "user",
                "content": "Painpoint = " + painpoint + "; Value Proposition = " + valueproposition + "; Persona = " + persona
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    text = ""
    for chunk in completion:
        text = text + str(chunk.choices[0].delta.content)
    st.markdown('**Elevator pitch =**')
    st.write(text)
else:
    st.write('Click the button to evaluate the prompt')