import os
import time
import pygame
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from deep_translator import GoogleTranslator

# Initialize pygame mixer
pygame.mixer.init()

isTranslateOn = False

# Language mapping
LANGUAGES = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Hindi": "hi",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
}

def get_language_code(language_name):
    """Convert language name to language code."""
    return LANGUAGES.get(language_name, "en")

def translator_function(spoken_text, from_language, to_language):
    """Translate text using GoogleTranslator from deep_translator."""
    try:
        return GoogleTranslator(source=from_language, target=to_language).translate(spoken_text)
    except Exception as e:
        return f"Translation Error: {str(e)}"

def text_to_voice(text_data, to_language):
    """Convert translated text to speech using gTTS."""
    try:
        myobj = gTTS(text=text_data, lang=to_language, slow=False)
        myobj.save("cache_file.mp3")
        audio = pygame.mixer.Sound("cache_file.mp3")
        audio.play()
        time.sleep(3)  # Wait for playback to finish
        os.remove("cache_file.mp3")
    except Exception as e:
        print(f"Text-to-Speech Error: {str(e)}")

def main_process(output_placeholder, from_language, to_language):
    """Speech-to-text, translation, and text-to-speech loop."""
    global isTranslateOn
    recognizer = sr.Recognizer()

    while isTranslateOn:
        with sr.Microphone() as source:
            output_placeholder.text("Listening...")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source, phrase_time_limit=10)

        try:
            output_placeholder.text("Processing...")
            spoken_text = recognizer.recognize_google(audio, language=from_language)

            output_placeholder.text("Translating...")
            translated_text = translator_function(spoken_text, from_language, to_language)

            text_to_voice(translated_text, to_language)
            output_placeholder.text(f"Translated: {translated_text}")

        except sr.UnknownValueError:
            output_placeholder.text("Could not understand the audio.")
        except sr.RequestError:
            output_placeholder.text("Could not request results. Check your internet connection.")
        except Exception as e:
            output_placeholder.text(f"Error: {str(e)}")

# Streamlit UI
st.title("Real-Time Language Translator")

from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.keys()))
to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.keys()))

from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

start_button = st.button("Start")
stop_button = st.button("Stop")

if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        output_placeholder = st.empty()
        main_process(output_placeholder, from_language, to_language)

if stop_button:
    isTranslateOn = False
