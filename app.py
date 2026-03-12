import streamlit as st
import os
import speech_recognition as sr
from gtts import gTTS

from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a helpful AI assistant. Answer clearly and concisely."),
        ("human", "Question: {question}")
    ]
)


def generate_response(question, llm_model, temperature, max_tokens):

    llm = Ollama(
        model=llm_model,
        temperature=temperature,
        num_predict=max_tokens
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser

    return chain.invoke({"question": question})


# 🎤 Voice input
def voice_input():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        st.write("🎤 Listening...")

        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text

        except:
            return "Could not understand audio"


# 🔊 Voice output
def speak(text):

    tts = gTTS(text)

    tts.save("response.mp3")

    audio_file = open("response.mp3", "rb")

    return audio_file


# Streamlit UI
st.title("🎤🤖 Voice Enabled AI Chatbot")


# Model selection
llm_model = st.sidebar.selectbox(
    "Select Model",
    ["tinyllama", "mistral", "phi3"]
)

temperature = st.sidebar.slider(
    "Temperature", 0.0, 1.0, 0.7
)

max_tokens = st.sidebar.slider(
    "Max Tokens", 50, 300, 150
)


# Text input
user_input = st.text_input("Type your question")


# Voice input button
if st.button("🎤 Speak"):

    user_input = voice_input()

    st.write("You said:", user_input)


if user_input:

    response = generate_response(
        user_input,
        llm_model,
        temperature,
        max_tokens
    )

    st.write("🤖:", response)

    # Voice output toggle
    if st.checkbox("🔊 Enable Voice Response"):

        audio_file = speak(response)

        st.audio(audio_file.read(), format="audio/mp3")