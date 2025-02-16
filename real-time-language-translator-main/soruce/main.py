import os
import pygame
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from googletrans import LANGUAGES, Translator

# Initialize the translator and pygame mixer
translator = Translator()
pygame.mixer.init()

# Create a mapping between language names and language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")
    audio.play()
    os.remove("cache_file.mp3")

# UI layout
st.title("Language Translator Chatbot")

# Input for user message
user_input = st.text_input("Write something to me:", "")

# Dropdowns for selecting languages
from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()), index=0)
to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()), index=1)

# Convert language names to language codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Button to submit the message
if st.button("Translate"):
    if user_input:
        # Translate the input text
        translated_text = translator_function(user_input, from_language, to_language)
        
        # Display the translated text
        st.text_area("Bot:", translated_text.text, height=150)

        # Convert translated text to speech
        text_to_voice(translated_text.text, to_language)

# Optional: Add a button for voice input
if st.button("Speak"):
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        st.text("Listening...")
        audio = rec.listen(source, phrase_time_limit=10)

    try:
        spoken_text = rec.recognize_google(audio, language=from_language)
        st.text_area("You:", spoken_text, height=150)

        # Translate the spoken text
        translated_text = translator_function(spoken_text, from_language, to_language)
        st.text_area("Bot:", translated_text.text, height=150)

       # Convert translated text to speech
        text_to_voice(translated_text.text, to_language)

    except Exception as e:
        st.error("Could not understand audio, please try again.")